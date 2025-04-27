import React, { useEffect, useState } from 'react';
import { View, Text, Button, StyleSheet, FlatList, Alert } from 'react-native';
import apiClient from '../services/api';
import * as SecureStore from 'expo-secure-store';
import * as DocumentPicker from 'expo-document-picker';
import * as FileSystem from 'expo-file-system';

export default function DashboardScreen({ navigation }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  const handleLogout = async () => {
    await SecureStore.deleteItemAsync('accessToken');
    await SecureStore.deleteItemAsync('refreshToken');
    navigation.replace('Login');
  };

  const fetchTasks = async () => {
    try {
      const payload = {
        "busy_slots": [
          { "start": "2025-04-26 10:00", "end": "2025-04-26 11:00", "title": "Meeting A" },
          { "start": "2025-04-26 14:00", "end": "2025-04-26 15:00", "title": "Meeting B" }
        ],
        "user_behavior": {
          "meal_prep_done": 0,
          "carpool_done": 1,
          "transit_done": 0,
          "grocery_spent": 45,
          "gas_spent": 20,
          "total_spent": 170
        },
        "timezone": "America/New_York"
      };
      console.log('📤 Sending payload:', payload);
      const { scheduled_tasks } = (await apiClient.post('/tasks/suggest', payload)).data;
      console.log('✅ Scheduled Tasks:', scheduled_tasks); // Debug the data
      setTasks(scheduled_tasks);
    } catch (error) {
      console.log('❌ Error fetching tasks:', error?.response?.data || error.message || error);
      Alert.alert('Error', 'Failed to fetch tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleUploadICS = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: 'text/calendar', // MIME type for .ics files
      });
  
      if (result.type === 'cancel') {
        console.log('❌ File selection canceled');
        return;
      }
  
      console.log('📤 Selected file:', result);
  
      // Send the file to the backend
      const formData = new FormData();
      formData.append('file', {
        uri: result.uri,
        name: result.name,
        type: result.mimeType || 'text/calendar', // Use the MIME type provided by DocumentPicker
      });
  
      const response = await apiClient.post('/calendar/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
  
      console.log('✅ Uploaded events:', response.data.events);
      Alert.alert('Success', 'Calendar uploaded successfully!');
      setTasks(response.data.events); // Update tasks with events from the calendar
    } catch (error) {
      console.error('❌ Error uploading .ics file:', error?.response?.data || error.message || error);
      Alert.alert('Error', 'Failed to upload calendar. Please try again.');
    }
  };

  const handleDownloadICS = async () => {
    try {
      const response = await apiClient.get('/calendar/download', {
        responseType: 'blob', // Ensure the response is treated as a file
      });

      // Save the file locally
      const url = URL.createObjectURL(new Blob([response.data], { type: 'text/calendar' }));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'calendar.ics');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);

      console.log('✅ Calendar downloaded successfully');
      Alert.alert('Success', 'Calendar downloaded successfully!');
    } catch (error) {
      console.error('❌ Error downloading calendar:', error?.response?.data || error.message || error);
      Alert.alert('Error', 'Failed to download calendar. Please try again.');
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const renderTaskCard = ({ item }) => {
    console.log('Rendering Task Card:', item); // Debug each task
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