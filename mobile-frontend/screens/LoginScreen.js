// screens/LoginScreen.js
import React, { useEffect } from 'react';
import {
  View,
  Text,
  Button,
  StyleSheet,
  ActivityIndicator,
  Alert,
} from 'react-native';
import * as AuthSession from 'expo-auth-session';
import * as SecureStore from 'expo-secure-store';

const AUTH0_DOMAIN    = 'dev-8ppo8q8eqvbtztw1.us.auth0.com';
const AUTH0_CLIENT_ID = 'CiBz194IWZHuq05Gplbpbsxrh1cYdDgk';
const AUTH0_AUDIENCE  = 'https://dev-8ppo8q8eqvbtztw1.us.auth0.com/api/v2/';

export default function LoginScreen({ navigation }) {
  // Build a proxy-friendly redirect URI for Expo Go
  const redirectUri = AuthSession.makeRedirectUri({
    scheme: 'saving-spree',
    useProxy: true,
  });

  // Discover Auth0 endpoints
  const discovery = AuthSession.useAutoDiscovery(`https://${AUTH0_DOMAIN}`);

  // Prepare the authentication request (PKCE is enabled by default)
  const [request, response, promptAsync] = AuthSession.useAuthRequest(
    {
      clientId: AUTH0_CLIENT_ID,
      redirectUri,
      scopes: ['openid', 'profile', 'email', 'offline_access'],
      extraParams: { audience: AUTH0_AUDIENCE },
    },
    discovery
  );

  // When the user completes the login in the browser, exchange the code for tokens
  useEffect(() => {
    if (response?.type === 'success' && request) {
      (async () => {
        try {
          const tokenResult = await AuthSession.exchangeCodeAsync(
            {
              clientId: AUTH0_CLIENT_ID,
              redirectUri,
              code: response.params.code,
              extraParams: {
                code_verifier: request.codeVerifier,
              },
            },
            discovery
          );

          if (tokenResult.accessToken) {
            // Persist tokens securely
            await SecureStore.setItemAsync('accessToken', tokenResult.accessToken);
            if (tokenResult.refreshToken) {
              await SecureStore.setItemAsync('refreshToken', tokenResult.refreshToken);
            }
            navigation.replace('Dashboard');
          } else {
            Alert.alert('Authentication Error', 'No access token returned');
          }
        } catch (err) {
          Alert.alert('Token Exchange Error', err.message);
        }
      })();
    }
  }, [response, request, redirectUri, discovery, navigation]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to SavingSpree</Text>

      {!request ? (
        <ActivityIndicator size="large" />
      ) : (
        <Button
          title="Login with Auth0"
          onPress={() => promptAsync({ useProxy: true })}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    marginBottom: 24,
    textAlign: 'center',
  },
});
