import ui.init_param_diag
import PyQt5.QtWidgets

if __name__ == '__main__':
    import sys
    APP = PyQt5.QtWidgets.QApplication(sys.argv)

    INIT_DIAG = ui.init_param_diag.Diag()
    INIT_DIAG.show()

    sys.exit(APP.exec_())
