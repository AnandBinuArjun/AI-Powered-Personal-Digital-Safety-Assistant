import 'package:flutter/material.dart';
import 'package:safety_assistant/screens/home_screen.dart';

void main() {
  runApp(const SafetyAssistantApp());
}

class SafetyAssistantApp extends StatelessWidget {
  const SafetyAssistantApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Safety Assistant',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const HomeScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}