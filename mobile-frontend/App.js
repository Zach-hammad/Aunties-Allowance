// App.js
import React, { useState, useEffect } from 'react';
import { ActivityIndicator, View } from 'react-native';
import * as SecureStore      from 'expo-secure-store';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import LoginScreen     from './screens/LoginScreen';
import DashboardScreen from './screens/DashboardScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  const [loading, setLoading]   = useState(true);
  const [isLoggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    (async () => {
      const token = await SecureStore.getItemAsync('accessToken');
      setLoggedIn(!!token);
      setLoading(false);
    })();
  }, []);

  if (loading) {
    return (
      <View style={{flex:1,justifyContent:'center',alignItems:'center'}}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Login"     component={LoginScreen}     />
        <Stack.Screen name="Dashboard" component={DashboardScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
