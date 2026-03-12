Инструкция по запуску проекта
1. Сборка пакета
bash
cd ~/ros2_ws
colcon build --packages-select exam_robot
source install/setup.bash
2. Запуск системы
bash
ros2 launch exam_robot robot_system.launch.py
3. Проверка работы
Визуализация в RViz:

bash
rviz2
Добавьте RobotModel и TF

Просмотр топиков:

bash
ros2 topic list
Проверка трансформаций:

bash
ros2 run tf2_tools view_frames.py
