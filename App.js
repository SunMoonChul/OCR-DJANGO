import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import React, { useState, useRef, useEffect } from 'react';

import LoginScreen from './LoginScreen';
import MainScreen from './MainScreen';
import IpContext from './IpContext';

const Stack = createStackNavigator();

export default function App() {

  const [ipRas, setIpRas] = useState('10.20.100.158');
  const [ipLap, setIpLap] = useState('10.20.102.148');
  const [ipLoc, setIpLoc] = useState('10.20.105.248');

  return (
    <IpContext.Provider value={{ ipRas, setIpRas, ipLap, setIpLap, ipLoc, setIpLoc }}>
      <NavigationContainer>
        <Stack.Navigator initialRouteName="Login" screenOptions={{ headerShown: false }}>
          <Stack.Screen name="Main" component={MainScreen} options={{ headerShown: false }}/>
          <Stack.Screen name="Login" component={LoginScreen}/>
        </Stack.Navigator>
      </NavigationContainer>
    </IpContext.Provider>
  );
}
