import React, { useState, useContext } from 'react';
import { View, TextInput, TouchableOpacity, StyleSheet, Image, Text, KeyboardAvoidingView } from 'react-native';
import { useNavigation, CommonActions } from '@react-navigation/native';
import axios from 'axios';
import IpContext from './IpContext';

export default function LoginScreen() {
    
    const context = useContext(IpContext);

    const [id, setId] = useState('');
    const [pw, setPw] = useState('');
    
    const navigation = useNavigation();

    const handleLogin = async () => {
        const data = {
            id: id,
            pw: pw
        };

        axios.post(`http://${context.ipLap}:3003/login`, data)
        .then(async response => {
            if (response.data.success) {
                navigation.navigate('Main');
            } else {
                alert(response.data.message); // 실패 메시지 표시
            }
        })
        .catch(error => {
            console.error(error);
        });
    };

    const handleJoin = () => {
        navigation.navigate('Join');
    };

    const handleID = () => {
        navigation.navigate('FindUserId');
    };

    const handlePW = () => {
        navigation.navigate('FindUserPW');
    };

    return (
        <KeyboardAvoidingView style={styles.container} behavior="padding">
            <Image
                source={require('./로고크롭.png')}
                style={styles.logo2}
                resizeMode="contain"
            />

            <TextInput
                style={styles.input}
                placeholder="Id"
                value={id}
                onChangeText={(text) => setId(text)}
            />
            <TextInput
                style={styles.input}
                placeholder="Pw"
                secureTextEntry={true}
                value={pw}
                onChangeText={(text) => setPw(text)}
            />
            <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
                <TouchableOpacity onPress={handleLogin} style={[styles.buttonContainer, { width: '40%' }]}>
                    <Text style={[styles.buttonText]}>Login</Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={handleJoin} style={[styles.buttonContainer, { width: '40%' }]}>
                    <Text style={[styles.buttonText]}>Sign up</Text>
                </TouchableOpacity>
            </View>

            <View style={{ height: 80 }} />
            <Text style={{ fontSize: 15 }}>Did you forget?</Text>
            <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
                <TouchableOpacity onPress={handleID} style={[styles.buttonContainer, { width: '40%' }]}>
                    <Text style={[styles.buttonText]}>Find ID</Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={handlePW} style={[styles.buttonContainer, { width: '40%' }]}>
                    <Text style={[styles.buttonText]}>Find PW</Text>
                </TouchableOpacity>
            </View>
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#3E83E0',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 16,
    },
    input: {
        width: "100%",
        height: 40,
        borderColor: "#3E6B39",
        borderWidth: 1,
        marginBottom: 12,
        paddingHorizontal: 8,
        borderRadius: 10,
    },
    logo: {
        width: '35%',
        height: 'auto',
        aspectRatio: 1,
        marginBottom: 10,
    },
    logo2: {
        width: '100%',
        height: 'auto',
        aspectRatio: 1,
        marginBottom: 10,
    },
    buttonContainer: {
        width: "80%",
        height: "auto",
        backgroundColor: "#98C593",
        paddingVertical: 10,
        borderRadius: 10,
        margin: 10,

        shadowColor: "#000",
        shadowOffset: { width: 0, height: -2 },
        shadowOpacity: .25,
        shadowRadius: 3.84,

        elevation: 5,
    },
    buttonText: {
        fontSize: 16,
        fontWeight: "bold",
        color: "#FFF",
        textAlign: "center",
    },
});
