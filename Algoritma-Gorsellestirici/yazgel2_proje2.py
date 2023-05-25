import sys
import random
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QSpinBox, QGridLayout, QWidget, QFormLayout, QRadioButton, QGroupBox
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class SortingVisualizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        

        

        self.init_ui()
        self.comparison_count = 0
        self.comparison_timer = QTimer()
        self.comparison_timer.timeout.connect(self.update_comparison_count)
        self.speed_scale = 1
        self.algorithm_complexity = {
            "Selection Sort": "O(n^2)",
            "Bubble Sort": "O(n^2)",
            "Insertion Sort": "O(n^2)",
            "Merge Sort": "O(n log n)",
            "Quick Sort": "O(n^2)",  # Worst case
        }
        self.sorting_algorithms = {
            "Selection Sort": self.selection_sort,
            "Bubble Sort": self.bubble_sort,
            "Insertion Sort": self.insertion_sort,
            "Merge Sort": self.merge_sort,
            "Quick Sort": self.quick_sort
        }
        self.visualization_types = {
            "Bar Chart": self.update_bar_chart,
            "Scatter Plot": self.update_scatter_plot,
            "Stem Plot": self.update_stem_plot
        }

    def init_ui(self):
        self.setWindowTitle("Sorting Visualizer")

        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        left_panel = self.create_left_panel()
        layout.addWidget(left_panel)

        # Algorithm Selection
        self.algorithm_selection = QComboBox()
        self.algorithm_selection.addItem("Selection Sort")
        self.algorithm_selection.addItem("Bubble Sort")
        self.algorithm_selection.addItem("Insertion Sort")
        self.algorithm_selection.addItem("Merge Sort")
        self.algorithm_selection.addItem("Quick Sort")

        # Speed Selection
        self.speed_selection = QSlider(Qt.Horizontal)
        self.speed_selection.setMinimum(1)
        self.speed_selection.setMaximum(5)
        self.speed_selection.setTickPosition(QSlider.TicksBothSides)
        self.speed_selection.setTickInterval(1)

        # List Input
        self.list_input = QLineEdit()

        # Start Button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_sorting)

        # Size Input
        self.manual_size_input = QRadioButton("Manual")
        self.random_size_input = QRadioButton("Random")
        size_group = QGroupBox("Size")
        size_layout = QVBoxLayout()
        size_layout.addWidget(self.manual_size_input)
        size_layout.addWidget(self.random_size_input)
        size_group.setLayout(size_layout)

        # Graph Type Selection
        self.graph_type_selection = QComboBox()
        self.graph_type_selection.addItem("Scatter")
        self.graph_type_selection.addItem("Bar")
        self.graph_type_selection.addItem("Stem")

        # Create-Start-Stop-Reset Buttons
        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.create_visualization)
        self.stop_button = QPushButton("Stop")
        self.reset_button = QPushButton("Reset")

        form_layout = QFormLayout()
        form_layout.addRow("Algorithm:", self.algorithm_selection)
        form_layout.addRow("Speed:", self.speed_selection)
        form_layout.addRow("List:", self.list_input)
        form_layout.addRow("", self.start_button)
        form_layout.addRow("Size:", size_group)
        form_layout.addRow("Graph Type:", self.graph_type_selection)
        form_layout.addRow("", self.create_button)
        form_layout.addRow("", self.stop_button)
        form_layout.addRow("", self.reset_button)

        layout.addLayout(form_layout)

        # Main panel visualization
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.comparison_label = QLabel("Comparisons: 0")
        layout.addWidget(self.comparison_label)

    def create_left_panel(self):
        left_panel = QWidget()
        layout = QVBoxLayout()

        # Input List
        input_list_label = QLabel("Input List")
        self.input_list_edit = QLineEdit()
        layout.addWidget(input_list_label)
        layout.addWidget(self.input_list_edit)

        # List Size
        size_label = QLabel("List Size")
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(1, 100)
        layout.addWidget(size_label)
        layout.addWidget(self.size_spinbox)

        # Speed
        speed_label = QLabel("Speed")
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["Slow", "Normal", "Fast"])
        self.speed_combo.currentIndexChanged.connect(self.change_speed)
        layout.addWidget(speed_label)
        layout.addWidget(self.speed_combo)

        # Sorting Algorithms
        algorithm_label = QLabel("Algorithm")
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(list(self.sorting_algorithms.keys()))
        self.algorithm_combo.currentIndexChanged.connect(self.change_algorithm)
        layout.addWidget(algorithm_label)
        layout.addWidget(self.algorithm_combo)

        # Visualization Types
        visualization_label = QLabel("Visualization")
        self.visualization_combo = QComboBox()
        self.visualization_combo.addItems(list(self.visualization_types.keys()))
        self.visualization_combo.currentIndexChanged.connect(self.change_visualization)
        layout.addWidget(visualization_label)
        layout.addWidget(self.visualization_combo)

        # Buttons
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_sorting)
        layout.addWidget(start_button)

        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.stop_sorting)
        layout.addWidget(stop_button)

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_visualization)
        layout.addWidget(reset_button)

        left_panel.setLayout(layout)
        return left_panel

    def change_speed(self, index):
        self.speed_scale = index + 1

    def change_algorithm(self, index):
        pass  # No need to do anything when the algorithm is changed

    def change_visualization(self, index):
        pass  # No need to do anything when the visualization is changed

    def create_visualization(self):
            plt.cla()  # Clear previous plot if any
            input_list = self.list_input.text().split(',')
            data = [int(x) for x in input_list if x]

            if not data:
                data = [random.randint(1, 100) for _ in range(10)]

            plt.bar(range(len(data)), data)
            self.canvas.draw()   

    def start_sorting(self):
        self.comparison_count = 0
        self.comparison_timer.start(3000)  # Update comparison count every 3 seconds

        selected_algorithm = self.algorithm_selection.currentText()
        speed = self.speed_selection.value()
        input_list = self.list_input.text()

        sorting_function = self.sorting_algorithms.get(selected_algorithm, None)

        if sorting_function:
            sorting_function(input_list, speed)

        # # Implement sorting algorithms and visualization here
        # print(f"Selected Algorithm: {selected_algorithm}")
        # print(f"Speed: {speed}")
        # print(f"Input List: {input_list}")

        # # Simulate sorting completion
        # self.sorting_completed(selected_algorithm)

    def stop_sorting(self):
        self.comparison_timer.stop()

    def reset_visualization(self):
        plt.cla()  # Clear previous plot
        self.canvas.draw()
        self.comparison_count = 0
        self.comparison_label.setText("Comparisons: 0")

    def update_comparison_count(self):
        self.comparison_count += 1
        self.comparison_label.setText(f"Comparisons: {self.comparison_count}")
    
    def sorting_completed(self, algorithm):
        self.comparison_timer.stop()
        complexity = self.algorithm_complexity.get(algorithm, "Unknown")
        print(f"Sorting completed. Comparisons: {self.comparison_count}, Algorithm Complexity: {complexity}")
    
    def selection_sort(self, input_list, speed):  #Selection Sort Start
        data = [int(x) for x in input_list.split(',') if x]

        if not data:
            data = [random.randint(1, 100) for _ in range(10)]

        for i in range(len(data)):
            min_index = i
            for j in range(i + 1, len(data)):
                self.update_comparison_count()
                if data[min_index] > data[j]:
                    min_index = j

            data[i], data[min_index] = data[min_index], data[i]
            self.update_bar_chart(data)
            QApplication.processEvents()

        self.sorting_completed("Selection Sort")    #Selection Sort End

    def bubble_sort(self, input_list, speed):  # Bubble Sort Start
        data = [int(x) for x in input_list.split(',') if x]

        if not data:
            data = [random.randint(1, 100) for _ in range(10)]

        for i in range(len(data)):
            for j in range(0, len(data) - i - 1):
                self.update_comparison_count()
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
                self.update_visualization(data)
                QApplication.processEvents()

        self.sorting_completed("Bubble Sort")    #Bubble Sort End

    def insertion_sort(self, input_list, speed):   #Insertion Sort Start
        data = [int(x) for x in input_list.split(',') if x]

        if not data:
            data = [random.randint(1, 100) for _ in range(10)]

        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >= 0 and data[j] > key:
                self.update_comparison_count()
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key
            self.update_visualization(data)
            QApplication.processEvents()

        self.sorting_completed("Insertion Sort")  #Insertion Sort End

    def merge_sort(self, data, left, right, speed):  #Merge Sort Start
        if left < right:
            middle = (left + right) // 2
            self.merge_sort(data, left, middle, speed)
            self.merge_sort(data, middle + 1, right, speed)
            self.merge(data, left, middle, right, speed)

    def merge(self, data, left, middle, right, speed):
        left_part = data[left:middle + 1]
        right_part = data[middle + 1:right + 1]

        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            self.update_comparison_count()
            if left_part[i] <= right_part[j]:
                data[k] = left_part[i]
                i += 1
            else:
                data[k] = right_part[j]
                j += 1
            k += 1

        while i < len(left_part):
            data[k] = left_part[i]
            i += 1
            k += 1

        while j < len(right_part):
            data[k] = right_part[j]
            j += 1
            k += 1

        self.update_visualization(data)
        QApplication.processEvents()      
        self.sorting_completed("Merge Sort") #Merge Sort End

    def quick_sort(self, data, low, high, speed):  #Quick Sort Start
        if low < high:
            pivot_index = self.partition(data, low, high, speed)
            self.quick_sort(data, low, pivot_index, speed)
            self.quick_sort(data, pivot_index + 1, high, speed)

    def partition(self, data, low, high, speed):
        pivot = data[low]
        left = low + 1
        right = high
        done = False

        while not done:
            while left <= right and data[left] <= pivot:
                self.update_comparison_count()
                left = left + 1

            while data[right] >= pivot and right >= left:
                self.update_comparison_count()
                right = right - 1

            if right < left:
                done = True
            else:
                data[left], data[right] = data[right], data[left]
                self.update_visualization(data)
                QApplication.processEvents()

        data[low], data[right] = data[right], data[low]
        self.update_visualization(data)
        QApplication.processEvents()
        self.sorting_completed("Quick Sort")  # Quick Start End

        return right

        

    def update_visualization(self, data):
        selected_visualization = self.visualization_selection.currentText()
        visualization_function = self.visualization_types.get(selected_visualization, None)

        if visualization_function:
            visualization_function(data)

    def update_bar_chart(self, data): #Bar Chart Start
        plt.cla()  # Clear previous plot
        plt.bar(range(len(data)), data)
        self.canvas.draw()           #Bar Chart End

    def update_scatter_plot(self, data):   #Scatter plot Start
        plt.cla()  # Clear previous plot
        plt.scatter(range(len(data)), data)
        self.canvas.draw()                 #Scatter plot Start

    def update_stem_plot(self, data):     #Stem plot Start
        plt.cla()  # Clear previous plot
        (markerline, stemlines, baseline) = plt.stem(range(len(data)), data, markerfmt='.')
        plt.setp(baseline, visible=False)
        plt.setp(stemlines, color='r', linewidth=1)
        plt.setp(markerline, markersize=6, markeredgewidth=1)
        self.canvas.draw()                #Stem plot Start

                         
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SortingVisualizerApp()
    window.show()
    sys.exit(app.exec_())