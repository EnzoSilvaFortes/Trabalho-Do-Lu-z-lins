import 'package:flutter/material.dart';
import 'dart:async';

void main() {
  runApp(const TrafficLightApp());
}

class TrafficLightApp extends StatelessWidget {
  const TrafficLightApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Semáforos Coordenados',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const TrafficLightPage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class TrafficLightPage extends StatefulWidget {
  const TrafficLightPage({super.key});

  @override
  State<TrafficLightPage> createState() => _TrafficLightPageState();
}

class _TrafficLightPageState extends State<TrafficLightPage> {
  final List<TrafficLight> trafficLights = [];
  Timer? _cycleTimer;
  int _currentGreenIndex = -1;
  bool _isRunning = false;
  int _extraTime = 0;

  @override
  void initState() {
    super.initState();
    for (int i = 0; i < 4; i++) {
      trafficLights.add(TrafficLight(id: i + 1));
    }
    _resetAllToRed();
  }

  @override
  void dispose() {
    _cycleTimer?.cancel();
    super.dispose();
  }

  void _resetAllToRed() {
    for (var light in trafficLights) {
      light.setState(TrafficLightState.red);
    }
  }

  void _startSystem() {
    setState(() {
      _isRunning = true;
      _extraTime = 0;
      _currentGreenIndex = -1;
      _resetAllToRed();
      _startNextCycle();
    });
  }

  void _stopSystem() {
    setState(() {
      _isRunning = false;
      _cycleTimer?.cancel();
      _resetAllToRed();
    });
  }

  void _startNextCycle() {
    if (!_isRunning) return;

    if (_currentGreenIndex >= 0) {
      trafficLights[_currentGreenIndex].setState(TrafficLightState.red);
    }

    _currentGreenIndex = (_currentGreenIndex + 1) % trafficLights.length;

    const int baseGreenTime = 15;
    final int totalGreenTime = baseGreenTime + _extraTime;
    _extraTime = 0;

    trafficLights[_currentGreenIndex].setState(TrafficLightState.green);
    setState(() {});

    _cycleTimer = Timer(Duration(seconds: totalGreenTime), () {
      if (!_isRunning) return;

      trafficLights[_currentGreenIndex].setState(TrafficLightState.yellow);
      setState(() {});

      _cycleTimer = Timer(const Duration(seconds: 3), () {
        _startNextCycle();
        setState(() {});
      });
    });
  }

  void _addExtraTime() {
    if (_isRunning && trafficLights[_currentGreenIndex].state == TrafficLightState.green) {
      setState(() {
        _extraTime += 1;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Controle de Semáforos'),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            children: [
              // Controles
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ElevatedButton(
                      onPressed: _isRunning ? _stopSystem : _startSystem,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: _isRunning ? Colors.red : Colors.green,
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                      ),
                      child: Text(
                        _isRunning ? 'PARAR' : 'INICIAR',
                        style: const TextStyle(fontSize: 14, color: Colors.white),
                      ),
                    ),
                    ElevatedButton(
                      onPressed: _addExtraTime,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blue,
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                      ),
                      child: const Text(
                        '+1s VERDE',
                        style: TextStyle(fontSize: 14, color: Colors.white),
                      ),
                    ),
                  ],
                ),
              ),
              
              // Tempo extra
              Padding(
                padding: const EdgeInsets.only(bottom: 8.0),
                child: Text(
                  'Tempo extra: $_extraTime segundos',
                  style: const TextStyle(fontSize: 14),
                ),
              ),
              
              // Semáforos - agora em uma grade mais compacta
              GridView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                padding: const EdgeInsets.all(4.0),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  crossAxisSpacing: 8,
                  mainAxisSpacing: 8,
                  childAspectRatio: 0.7, // Proporção mais compacta
                ),
                itemCount: trafficLights.length,
                itemBuilder: (context, index) {
                  return TrafficLightWidget(
                    trafficLight: trafficLights[index],
                    isActive: index == _currentGreenIndex && _isRunning,
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}

enum TrafficLightState { red, yellow, green }

class TrafficLight {
  final int id;
  TrafficLightState _state = TrafficLightState.red;

  TrafficLight({required this.id});

  TrafficLightState get state => _state;

  void setState(TrafficLightState newState) {
    _state = newState;
  }
}

class TrafficLightWidget extends StatelessWidget {
  final TrafficLight trafficLight;
  final bool isActive;

  const TrafficLightWidget({
    super.key,
    required this.trafficLight,
    required this.isActive,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'Semáforo ${trafficLight.id}',
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.bold,
                color: isActive ? Colors.blue : Colors.grey,
              ),
            ),
            const SizedBox(height: 8),
            // Container do semáforo reduzido
            Container(
              width: 60,  // Largura reduzida
              height: 120, // Altura reduzida
              decoration: BoxDecoration(
                color: Colors.grey[800],
                borderRadius: BorderRadius.circular(10),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  // Luzes com tamanho reduzido
                  _buildLight(Colors.red, trafficLight.state == TrafficLightState.red, 30),
                  _buildLight(Colors.yellow, trafficLight.state == TrafficLightState.yellow, 30),
                  _buildLight(Colors.green, trafficLight.state == TrafficLightState.green, 30),
                ],
              ),
            ),
            const SizedBox(height: 4),
            Text(
              _getStateText(trafficLight.state),
              style: const TextStyle(fontSize: 12),
            ),
          ],
        ),
      ),
    );
  }

  String _getStateText(TrafficLightState state) {
    switch (state) {
      case TrafficLightState.red: return 'Vermelho';
      case TrafficLightState.yellow: return 'Amarelo';
      case TrafficLightState.green: return 'Verde';
    }
  }

  Widget _buildLight(Color color, bool isOn, double size) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        color: isOn ? color : Colors.black.withOpacity(0.3),
        shape: BoxShape.circle,
        border: Border.all(color: Colors.white, width: 1),
        boxShadow: isOn
            ? [BoxShadow(color: color.withOpacity(0.8), blurRadius: 6, spreadRadius: 1)]
            : null,
      ),
    );
  }
}