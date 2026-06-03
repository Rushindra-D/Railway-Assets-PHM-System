🚆 Real-Time Prognostics and Health Management (PHM) of Railway Assets Using Unsupervised Machine Learning
📌 Project Overview

This project presents an intelligent Prognostics and Health Management (PHM) framework for railway mechanical assets using unsupervised machine learning techniques.
Traditional predictive maintenance systems often depend on labeled failure data or detailed physical degradation models, which are expensive and difficult to obtain in real-world railway environments. To address this challenge, this project proposes a data-driven approach that learns normal operating behavior directly from sensor data and identifies deviations that may indicate asset degradation.

🎯 Problem Statement

Railway assets such as bearings, wheelsets, traction systems, and braking components are subjected to continuous operational stress and degradation.

Conventional maintenance strategies face several limitations:

Reactive maintenance leads to unexpected breakdowns.
Scheduled maintenance can result in unnecessary servicing.
Failure data is often scarce or unavailable.
Physical degradation models may not generalize across assets.

The need for intelligent maintenance systems has led to the development of data-driven PHM solutions capable of identifying degradation patterns before failures occur.

🚀 Proposed Solution

The proposed system uses the Isolation Forest algorithm to learn normal operating conditions from sensor data and detect abnormal behavior without requiring labeled fault data.

The workflow includes:

Sensor Data Acquisition
Data Preprocessing
Anomaly Detection using Isolation Forest
Health Index Generation
Degradation Trend Analysis
Remaining Useful Life (RUL) Estimation
Maintenance Decision Support

✨ Key Features
Unsupervised anomaly detection
Real-time asset health monitoring
Health Index (HI) generation
Remaining Useful Life (RUL) estimation
Early fault detection
Predictive maintenance support
Maintenance decision assistance
Interactive dashboard visualization

📊 Dataset

The framework is validated using time-sequenced bearing vibration data due to its well-defined progressive degradation behavior.

Dataset Characteristics
Sequential sensor measurements
Progressive mechanical degradation
Continuous monitoring simulation
Suitable for PHM applications

The framework can be adapted to:

Bearings
Wheelsets
Traction Motors
Brake Systems
Gearboxes
Other railway mechanical assets

🛠️ Technology Stack
Programming Language
Python
Machine Learning
Scikit-Learn
Isolation Forest
Data Processing
Pandas
NumPy
Visualization
Matplotlib
Plotly

📈 Outputs

The system provides:

Anomaly Detection
Normal Condition
Warning Condition
Critical Condition
Health Index (HI)
Continuous asset health monitoring
Degradation trend visualization
Remaining Useful Life (RUL)
Estimated lifespan before failure
Maintenance scheduling support
Maintenance Alerts
Early warning notifications
Fault risk indicators

🔮 Future Enhancements
IoT sensor integration
Deep learning-based prognostics
Digital Twin implementation
Multi-asset fleet monitoring
Edge AI deployment
Real-time railway monitoring systems

📷 Results
Anomaly Detection Dashboard

Displays abnormal operating conditions and identifies potential degradation at an early stage.

Health Index Visualization

Shows asset health progression and degradation trends over time.

Remaining Useful Life Prediction

Provides estimated operational life remaining before maintenance is required.

Maintenance Alert System

Generates timely alerts and maintenance recommendations based on asset condition.
