import sys, os, traceback
print('cwd', os.getcwd())
print('in sys.path', os.getcwd() in sys.path)
print('backend exists', os.path.isdir('backend'))
try:
    import backend
    print('backend', backend)
    import backend.config
    print('backend.config loaded')
except Exception as e:
    traceback.print_exc()
