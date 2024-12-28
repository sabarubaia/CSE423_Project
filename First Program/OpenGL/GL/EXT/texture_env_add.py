'''OpenGL extension EXT.texture_env_add

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.texture_env_add to provide a more 
Python-friendly API

Overview (from the spec)
	
	New texture environment function ADD is supported with the following 
	equation: 
	                    Cv = min(1, Cf + Ct)
	
	New function may be specified by calling TexEnv with ADD token.
	

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/texture_env_add.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.texture_env_add import *
from OpenGL.raw.GL.EXT.texture_env_add import _EXTENSION_NAME

def glInitTextureEnvAddEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION