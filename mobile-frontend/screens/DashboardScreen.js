import React, { useEffect, useState } from 'react';
import { View, Text, Button, StyleSheet, FlatList, Alert } from 'react-native';
import apiClient from '../services/api';
import * as SecureStore from 'expo-secure-store';
import * as DocumentPicker from 'expo-document-picker';
import * as FileSystem from 'expo-file-system';
import * as Sharing from 'expo-sharing';

export default function DashboardScreen({ navigation }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [userInputs, setUserInputs] = useState({
    meal_prep_done: 0,
    carpool_done: 0,
    transit_done: 0
  });

  const handleLogout = async () => {
    await SecureStore.deleteItemAsync('accessToken');
    await SecureStore.deleteItemAsync('refreshToken');
    navigation.replace('Login');
  };

  // Improved calendar upload function
  const handleUploadICS = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: 'text/calendar',
      });

      if (result.canceled) {
        console.log('❌ File selection canceled');
        return;
      }

      // Get file info
      const fileUri = result.assets[0].uri;
      const fileName = result.assets[0].name;
      
      // Create FormData object - note the field name 'file' should match what the backend expects
      const formData = new FormData();
      formData.append('calendar', {
        uri: fileUri,
        name: fileName,
        type: 'text/calendar'
      });
      
      console.log('📤 Uploading calendar file:', fileName);
      
      // Send to backend
      const response = await apiClient.post('/calendar/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('✅ Calendar uploaded successfully');
      
      // Handle the busy slots returned from the backend
      if (response.data.busy_slots) {
        const busySlots = response.data.busy_slots;
        
        // Save busy slots to storage for later use
        await SecureStore.setItemAsync('busySlots', JSON.stringify(busySlots));
        
        // Immediately use these slots to fetch task suggestions
        await fetchTasksWithBusySlots(busySlots, userInputs);
      }
      
      Alert.alert('Success', 'Calendar uploaded and processed successfully!');
    } catch (error) {
      console.error('❌ Error uploading calendar:', error?.response?.data || error.message || error);
      Alert.alert('Error', 'Failed to upload calendar. Please try again.');
    }
  };

  // Fetch Plaid financial data
  const fetchPlaidData = async () => {
    try {
      // Get Plaid access token from secure storage
      const accessToken = await SecureStore.getItemAsync('plaidAccessToken');
      
      if (!accessToken) {
        console.log('No Plaid access token found, using default values');
        return null;
      }
      
      // Calculate date range (e.g., last 30 days)
      const endDate = new Date().toISOString().split('T')[0]; // Today
      const startDate = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]; // 30 days ago
      
      console.log('📊 Fetching Plaid transaction data');
      
      // Fetch transactions from Plaid
      const response = await apiClient.post('/plaid/transactions', {
        access_token: accessToken,
        start_date: startDate,
        end_date: endDate
      });
      
      console.log('✅ Plaid data retrieved:', response.data.transactions?.length || 0, 'transactions');
      
      return response.data;
    } catch (error) {
      console.log('❌ Error fetching Plaid transactions:', error?.response?.data || error.message || error);
      return null;
    }
  };

  // Updated function to fetch tasks using busy slots and user inputs
  // Updated function to fetch tasks using busy slots and Plaid data
const fetchTasksWithBusySlots = async (busySlots) => {
  try {
    // Get user's timezone
    const timezone = Intl.DateTimeFormat().resolvedOptions().timezone || "America/New_York";
    
    // Initialize userBehavior with default values
    let userBehavior = {
      meal_prep_done: 0,
      carpool_done: 0,
      transit_done: 0,
      grocery_spent: 0,
      gas_spent: 0,
      total_spent: 0
    };
    
    // Try to get user inputs from form or state
    // You can implement UI elements to collect these inputs
    const formValues = {
      meal_prep_done: 1,  // Replace with actual form values
      carpool_done: 0,    // Replace with actual form values
      transit_done: 1     // Replace with actual form values
    };
    
    // Update behavior with form values
    userBehavior = {
      ...userBehavior,
      ...formValues
    };
    
    // Try to get financial data from Plaid
    try {
      // Get Plaid access token
      const plaidAccessToken = await SecureStore.getItemAsync('plaidAccessToken');
      
      if (plaidAccessToken) {
        // Request Plaid transaction data from your backend
        const plaidResponse = await apiClient.post('/plaid/transactions', {
          access_token: plaidAccessToken
        });
        
        if (plaidResponse.data && plaidResponse.data.transactions) {
          const transactions = plaidResponse.data.transactions;
          
          // Calculate spending by category - make sure the categories match what Plaid returns
          const groceryTransactions = transactions.filter(t => 
            t.category && t.category.some(cat => cat.includes('Groceries') || cat.includes('Food')));
            
          const gasTransactions = transactions.filter(t => 
            t.category && t.category.some(cat => cat.includes('Gas') || cat.includes('Fuel')));
          
          // Sum up transaction amounts
          userBehavior.grocery_spent = Math.round(groceryTransactions.reduce((sum, t) => sum + Math.abs(t.amount), 0));
          userBehavior.gas_spent = Math.round(gasTransactions.reduce((sum, t) => sum + Math.abs(t.amount), 0));
          userBehavior.total_spent = Math.round(transactions.reduce((sum, t) => sum + Math.abs(t.amount), 0));
          
          console.log('📊 Plaid data processed:', {
            grocery: userBehavior.grocery_spent,
            gas: userBehavior.gas_spent,
            total: userBehavior.total_spent
          });
        }
      }
    } catch (plaidError) {
      console.log('❌ Error with Plaid data:', plaidError);
      // Fall back to stored values
      try {
        const savedBehavior = await SecureStore.getItemAsync('userBehavior');
        if (savedBehavior) {
          const parsedBehavior = JSON.parse(savedBehavior);
          // Keep user inputs but use saved financial data
          userBehavior.grocery_spent = parsedBehavior.grocery_spent || 45;
          userBehavior.gas_spent = parsedBehavior.gas_spent || 20;
          userBehavior.total_spent = parsedBehavior.total_spent || 170;
        }
      } catch (e) {
        console.log('No saved user behavior found, using defaults');
        userBehavior.grocery_spent = 45;
        userBehavior.gas_spent = 20;
        userBehavior.total_spent = 170;
      }
    }
    
    // Make sure to structure the payload correctly for the backend
    const payload = {
      busy_slots: busySlots,
      user_behavior: userBehavior,
      timezone: timezone
    };
    
    console.log('📤 Sending task suggestion payload:', payload);
    
    const response = await apiClient.post('/tasks/suggest', payload);
    const { scheduled_tasks, ics_file_path } = response.data;
    
    console.log('✅ Received scheduled tasks:', scheduled_tasks.length);
    
    // Save the ICS file path for download
    if (ics_file_path) {
      await SecureStore.setItemAsync('icsFilePath', ics_file_path);
    }
    
    // Save the latest user behavior for future reference
    await SecureStore.setItemAsync('userBehavior', JSON.stringify(userBehavior));
    
    setTasks(scheduled_tasks);
  } catch (error) {
    console.log('❌ Error suggesting tasks:', error?.response?.data || error.message || error);
    throw error; // Re-throw to be handled by the caller
  }
};

  // Updated fetch tasks function to use stored busy slots and user inputs
  const fetchTasks = async () => {
    try {
      setLoading(true);
      
      // Try to get busy slots from storage
      let busySlots = [];
      try {
        const savedSlots = await SecureStore.getItemAsync('busySlots');
        if (savedSlots) {
          busySlots = JSON.parse(savedSlots);
        }
      } catch (e) {
        console.log('No saved busy slots found');
      }
      
      // If we have busy slots, use them for task suggestions
      if (busySlots.length > 0) {
        await fetchTasksWithBusySlots(busySlots, userInputs);
      } else {
        // Create fallback busy slots for initial experience
        const currentDate = new Date();
        const formattedDate = currentDate.toISOString().split('T')[0]; // YYYY-MM-DD
        
        const defaultBusySlots = [
          { 
            start: `${formattedDate} 10:00`, 
            end: `${formattedDate} 11:00`, 
            title: "Morning Routine" 
          },
          { 
            start: `${formattedDate} 14:00`, 
            end: `${formattedDate} 15:00`, 
            title: "Afternoon Break" 
          }
        ];
        
        await fetchTasksWithBusySlots(defaultBusySlots, userInputs);
      }
    } catch (error) {
      console.log('❌ Error fetching tasks:', error?.response?.data || error.message || error);
      Alert.alert('Error', 'Failed to fetch tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Improved download function to use the stored file path
  const handleDownloadICS = async () => {
    try {
      // Get the file path from storage
      const icsFilePath = await SecureStore.getItemAsync('icsFilePath');
      
      if (!icsFilePath) {
        throw new Error('No calendar file available for download');
      }
      
      // Get base URL
      const baseUrl = apiClient.defaults.baseURL || '';
      
      // Path to save the downloaded file
      const fileUri = FileSystem.documentDirectory + 'weekly_plan.ics';
      
      // Download the file
      const downloadResult = await FileSystem.downloadAsync(
        `${baseUrl}/calendar/download`,
        fileUri,
        {
          headers: {
            Authorization: `Bearer ${await SecureStore.getItemAsync('accessToken')}`
          }
        }
      );
      
      if (downloadResult.status !== 200) {
        throw new Error(`Download failed with status ${downloadResult.status}`);
      }
      
      // Share the file
      await Sharing.shareAsync(fileUri, {
        mimeType: 'text/calendar',
        dialogTitle: 'Save or Share Your Schedule'
      });
      
      console.log('✅ Calendar downloaded and shared successfully');
      Alert.alert('Success', 'Calendar downloaded successfully!');
    } catch (error) {
      console.error('❌ Error downloading calendar:', error);
      if (error.message?.includes('No calendar')) {
        Alert.alert('Error', 'No weekly plan has been generated yet. Please upload a calendar first.');
      } else {
        Alert.alert('Error', 'Failed to download calendar. Please try again.');
      }
    }
  };

  // Function to update user inputs (for an input form)
  const handleUserInputChange = (field, value) => {
    setUserInputs(prev => ({
      ...prev,
      [field]: value
    }));
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const renderTaskCard = ({ item }) => {
    return (
      <View style={styles.card}>
        <Text style={styles.task}>{item.task || item.summary}</Text>
        <Text style={styles.time}>
          {item.scheduled_day || item.start} | {item.start_time || item.start} - {item.end_time || item.end}
        </Text>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>📝 Your Weekly Plan</Text>

      {loading ? (
        <Text style={styles.loadingText}>Loading tasks...</Text>
      ) : tasks.length > 0 ? (
        <FlatList
          data={tasks}
          keyExtractor={(item, index) => index.toString()}
          renderItem={renderTaskCard}
          contentContainerStyle={styles.list}
        />
      ) : (
        <Text style={styles.loadingText}>No tasks found. 🎯</Text>
      )}

      <Button title="Upload .ics File" onPress={handleUploadICS} />
      <Button title="Download Calendar" onPress={handleDownloadICS} />
      <Button title="Logout" onPress={handleLogout} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8f9fa', padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  list: { paddingBottom: 20 },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 10,
    padding: 20,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 8,
    elevation: 5,
  },
  task: { fontSize: 20, fontWeight: '600', marginBottom: 8 },
  time: { fontSize: 16, color: '#6c757d' },
  loadingText: { textAlign: 'center', marginTop: 20, fontSize: 16 },
});