import React, { useState, useEffect, useContext } from 'react';
import { StyleSheet, Text, TouchableOpacity, View, Button, ImageBackground, Alert } from 'react-native';
import { useNavigation, CommonActions } from '@react-navigation/native';
import IpContext from './IpContext';
import * as Location from 'expo-location';
import axios from 'axios';

export default function Main() {

    const context = useContext(IpContext);

    const [speed, setSpeed] = useState(0);
    const [prevSpeed, setPrevSpeed] = useState(0); // 이전 속도
    const [latitude, setLatitude] = useState(null);
    const [longitude, setLongitude] = useState(null);
    const [message, setMessage] = useState(''); // 급가속 또는 급정거 메시지
    const [cnt, setCnt] = useState(0); // 급가속 또는 급정거 횟수
    const user = 'qwer';
    const address = `http://${context.ipLap}:8000/example/`;

    const navigation = useNavigation();

    const runVideoScript = () => {
        axios
            .post(`http://${context.ipRas}:5000/run-video`)
            .then((response) => console.log(response))
            .catch((error) => console.error(error));
        Alert.alert('영상촬영 start(❁´◡`❁)');
    };
    const stopVideoScript = () => {
        axios
            .post(`http://${context.ipRas}:5000/run-video`)
            .then((response) => console.log(response))
            .catch((error) => console.error(error));
        Alert.alert('영상전송완료~~(((o(*ﾟ▽ﾟ*)o)))');
    };

    useEffect(() => {
        (async () => {
            let { status } = await Location.requestForegroundPermissionsAsync();
            if (status !== 'granted') {
                console.log('Permission to access location was denied');
                return;
            }

            const watchId = await Location.watchPositionAsync(
                {
                    accuracy: Location.Accuracy.High,
                    timeInterval: 100, // 위치정보 업데이트 간격 1초 안의
                    distanceInterval: 0, // 위치 변할 때마다 알림
                },
                (position) => {
                    const currentSpeed = position.coords.speed * 3.6;

                    // 속도가 1초 이내에 20km 이상 올라가면 '급가속'
                    if (currentSpeed - prevSpeed >= 10) {
                        setMessage('급가속');
                        setCnt((cnt) => cnt + 1); // 카운트 증가
                        console.log('급가속');
                        console.log(address + 'accel/');
                        // 여기에서 서버에 데이터를 전송합니다.
                        axios
                            .post(address + 'accel/', {
                                user: user,
                            })
                            .then((response) => {
                                console.log(response.data)
                                console.log('급가속 완');
                            })
                            .catch((error) => {
                                console.error(error)
                            });
                    }
                    // 속도가 1초 이내에 20km 이상 내려가면 '급정거'
                    else if (prevSpeed - currentSpeed >= 10) {
                        setMessage('급정거');
                        setCnt((cnt) => cnt + 1); // 카운트 증가
                        console.log('급정거');
                        // 여기에서 서버에 데이터를 전송합니다.
                        axios
                            .post(address + 'deccel/', {
                                user: user,
                            })
                            .then((response) => console.log(response.data))
                            .catch((error) => console.error(error));
                        console.log(address + 'deccel/');
                        console.log('급정거 완');
                    } else {
                        setMessage('');
                    }

                    setPrevSpeed(speed); // 이전 속도 업데이트
                    setSpeed(currentSpeed);
                    setLatitude(position.coords.latitude);
                    setLongitude(position.coords.longitude);
                }
            );

            return () => watchId.remove();
        })();
    }, []);

    return (
        <ImageBackground source={require('./b1.jpg')} style={styles.image}>
            <View style={styles.container}>
                <Button title="Run Video Script" onPress={runVideoScript} />
                <Button title="Stop Video Script" onPress={stopVideoScript} />
            </View>
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                <Text>현재 속도: {speed.toFixed(2)} km/h</Text>
                {latitude && <Text>위도: {latitude.toFixed(6)}</Text>}
                {longitude && <Text>경도: {longitude.toFixed(6)}</Text>}
                {/* 급가속 또는 급정거 메시지를 <Text> 컴포넌트로 감쌉니다. */}
                {message && <Text>{message}</Text>}
                {/* 급가속 또는 급정거 횟수를 표시합니다. */}
                {<Text>급가속/급정거 횟수: {cnt}</Text>}
            </View>
        </ImageBackground>
    );
}
const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
    },
    image: {
        flex: 1,
        resizeMode: 'cover',
        justifyContent: 'center',
    },
});