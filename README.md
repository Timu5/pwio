# PWIO

Program draws fractal (the boundary of the Mandelbrot set) step by step with multi-threading.
There are two modes: with executor usage and classical multi-threading.
Global interpreter lock (GIL) prevents multiple threads from executing Python bytecodes at once.
This mechanism prevents from race condition and ensures thread safety.
In this project GIL was disabled in order to enable running multiple threads. 
To make it possible numba (JIT complier) was used.

![animacja4](https://user-images.githubusercontent.com/41776275/111493193-9f484300-873d-11eb-9fbd-5ec78683994c.gif)



## Getting Started

To get a local copy and run this program, follow these steps.

### Prerequisites

Python 3.9 should be already installed on your computer.

### Installation

1. Clone the repo:

```
git clone https://github.com/Timu5/pwio.git
```

2. Install dependencies:

```
pip install numba opencv-python
```
3. Run program:

```
python3 main.py
```

## License

Distributed under the MIT License.

