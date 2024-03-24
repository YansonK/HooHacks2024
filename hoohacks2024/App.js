import React, { useEffect, useState } from 'react';
import { View, Text, Image, ScrollView, TextInput, StyleSheet, TouchableOpacity, Dimensions, ImageBackground} from 'react-native';

export default function App() {
  const [stationsData, setStationsData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch('http://172.25.167.129:5000/api/stations') // replace with your Flask API endpoint
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setStationsData(data))
      .catch(error => console.error('There has been a problem with your fetch operation: ', error));
  }, []);
  

  const diningHalls = [
    { name: 'O-Hill', image: 'https://branchbuilds.com/wp-content/uploads/2021/09/observatory-hill-03.jpg', Stations: stationsData[0] },
    { name: 'FFC', image: 'https://www.coleanddenny.com/wp-content/uploads/2020/07/HDPhoto_130723_07_FS1.jpg', Stations: stationsData[1] },
    { name: 'Runk', image: 'https://tipton-associates.com/wp-content/uploads/2020/09/RunkDiningHall_Img1.jpg', Stations: stationsData[2] },
  ];

  // Get the screen width
  const screenWidth = Dimensions.get('window').width;

  // Calculate the number of columns: use 1 for small devices and 2 for large devices
  const numColumns = screenWidth > 500 ? 2 : 1;

  // Calculate the width of each dining hall container
  const containerWidth = (screenWidth - 40) / numColumns - 10;

  if (isLoading) {
    return <Text>Loading...</Text>; 
  }

  return (
    <View style={styles.container}>
      <ImageBackground source={{ uri: 'https://media.licdn.com/dms/image/D4E16AQEhhFL-_sZ_xQ/profile-displaybackgroundimage-shrink_200_800/0/1667594600063?e=2147483647&v=beta&t=bWvcgGTNQOcJBh7nuRQmjOt1YF6N3rHr6aiNxcJpDWo' }} style={styles.topBar}></ImageBackground>
      <View style={styles.chipContainer}>
        {['Egg', 'Milk', 'Other'].map((chip, index) => (
          <TouchableOpacity key={index} style={styles.chip}>
            <Text>{chip}</Text>
          </TouchableOpacity>
        ))}
      </View>
      <Text style={styles.title}>Dining Halls</Text>
      <ScrollView contentContainerStyle={styles.diningHallList}>
        {diningHalls.map((diningHall, index) => (
          <TouchableOpacity key={index} style={[styles.diningHallContainer, { width: containerWidth }]}>
            <Image source={{ uri: diningHall.image }} style={styles.diningHallImage} />
            <Text style={styles.diningHallName}>{diningHall.name}</Text>
            <Text style={styles.diningHallStations}>{diningHall.Stations} Available Stations</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
}



const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  topBar: {
    height: Dimensions.get('window').height/6,
    width: '100%',
  },
  chipContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginVertical: 10,
    marginHorizontal: 20,
  },
  chip: {
    padding: 10,
    borderColor: 'gray',
    borderWidth: 1,
    borderRadius: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
  },
  diningHallList: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-around', // centers items horizontally
    alignItems: 'center', // centers items vertically
  },
  diningHallContainer: {
    width: '48%',
    borderColor: 'gray',
    borderWidth: 1,
    borderRadius: 10,
    marginBottom: 10,
    padding: 10,
    alignItems: 'center',
  },
  diningHallName: {
    paddingTop: 10,
    fontSize: 18,
    marginBottom: 10,
  },
  diningHallImage: {
    width: '100%',
    height: 100,
  },
  diningHallStations: {
    fontSize: 12,
    color: 'gray',
    position: 'absolute',
    bottom:20,
    left: 10,
  },
});
