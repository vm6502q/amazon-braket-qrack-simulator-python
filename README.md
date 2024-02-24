# Amazon Braket (SDK) Qrack Simulator

This is an Amazon Braket SDK back end for the open-source [unitaryfund/qrack](https://github.com/unitaryfund/qrack) simulator. ([PyQrack](https://github.com/unitaryfund/pyqrack) provides pure Python language bindings from C++ Qrack.) This simulator can be run locally, via either a (vendor-agnostic) OpenCL implementation or a (NVIDIA-specific) CUDA implementation. (CPU-only local simulation is also supported, when compiling and installing Qrack from source.) You can use the simulator to test quantum tasks that you construct for the [Amazon Braket SDK](https://github.com/amazon-braket/amazon-braket-sdk-python) before you submit them to the Amazon Braket service for execution.

## Setting up Amazon Braket Qrack Simulator Python
Installing this package will install the [Amazon Braket SDK](https://github.com/amazon-braket/amazon-braket-sdk-python), necessary to use the local simulator.
For manual installation of the SDK, follow the instructions in the [README](https://github.com/amazon-braket/amazon-braket-sdk-python/blob/main/README.md) for setup.

**Checking the version of the Qrack simulator**

You can check your currently installed version of `amazon-braket-qrack-simulator` with `pip show`:

```bash
pip show amazon-braket-qrack-simulator
```

or alternatively from within Python:

```
>>> from braket import qrack_simulator
>>> qrack_simulator.__version__
```

## Usage
The quantum simulator implementation `BraketQrackSimulator` plugs into the `LocalSimulator` interface in 
[Amazon Braket SDK](https://github.com/amazon-braket/amazon-braket-sdk-python), with the `backend` parameter as `"qrack"`.

**Executing a circuit using the default simulator**
```python
from braket.circuits import Circuit
from braket.devices import LocalSimulator

device = LocalSimulator(backend="qrack")

bell = Circuit().h(0).cnot(0, 1)
print(device.run(bell, shots=100).result().measurement_counts)
```

## Documentation

`BraketQrackSimulator` follows a subset of the [Amazon Braket SDK](https://github.com/amazon-braket/amazon-braket-sdk-python) default simulator input and output interfaces. Detailed documentation for the default simulator, including the API reference, can be found on [Read the Docs](https://amazon-braket-default-simulator-python.readthedocs.io/en/latest/).

**To generate the API Reference HTML in your local environment**

First, install tox:

```bash
pip install tox
```

To generate the HTML, first change directories (`cd`) to position the cursor in the `amazon-braket-qrack-simulator-python` directory. Then, run the following command to generate the HTML documentation files:

```bash
tox -e docs
```

To view the generated documentation, open the following file in a browser:
`../amazon-braket-qrack-simulator-python/build/documentation/html/index.html`

## Testing

If you want to contribute to the project, be sure to run unit tests and get a successful result 
before you submit a pull request. To run the unit tests, first install `pytest`, if necessary:

```bash
pip install pytest
```

With pytest installed, use this command in the `amazon-braket-qrack-simulator-python` directory:

```bash
pytest .
```

## License

This project is licensed under the Apache-2.0 License.

