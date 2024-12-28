'''OpenGL extension VERSION.GL_1_3

This module customises the behaviour of the 
OpenGL.raw.GL.VERSION.GL_1_3 to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/VERSION/GL_1_3.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.VERSION.GL_1_3 import *
from OpenGL.raw.GL.VERSION.GL_1_3 import _EXTENSION_NAME

def glInitGl13VERSION():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glCompressedTexImage3D.data size not checked against imageSize
glCompressedTexImage3D=wrapper.wrapper(glCompressedTexImage3D).setInputArraySize(
    'data', None
)
# INPUT glCompressedTexImage2D.data size not checked against imageSize
glCompressedTexImage2D=wrapper.wrapper(glCompressedTexImage2D).setInputArraySize(
    'data', None
)
# INPUT glCompressedTexImage1D.data size not checked against imageSize
glCompressedTexImage1D=wrapper.wrapper(glCompressedTexImage1D).setInputArraySize(
    'data', None
)
# INPUT glCompressedTexSubImage3D.data size not checked against imageSize
glCompressedTexSubImage3D=wrapper.wrapper(glCompressedTexSubImage3D).setInputArraySize(
    'data', None
)
# INPUT glCompressedTexSubImage2D.data size not checked against imageSize
glCompressedTexSubImage2D=wrapper.wrapper(glCompressedTexSubImage2D).setInputArraySize(
    'data', None
)
# INPUT glCompressedTexSubImage1D.data size not checked against imageSize
glCompressedTexSubImage1D=wrapper.wrapper(glCompressedTexSubImage1D).setInputArraySize(
    'data', None
)
# OUTPUT glGetCompressedTexImage.img COMPSIZE(target, level) 
glMultiTexCoord1dv=wrapper.wrapper(glMultiTexCoord1dv).setInputArraySize(
    'v', 1
)
glMultiTexCoord1fv=wrapper.wrapper(glMultiTexCoord1fv).setInputArraySize(
    'v', 1
)
glMultiTexCoord1iv=wrapper.wrapper(glMultiTexCoord1iv).setInputArraySize(
    'v', 1
)
glMultiTexCoord1sv=wrapper.wrapper(glMultiTexCoord1sv).setInputArraySize(
    'v', 1
)
glMultiTexCoord2dv=wrapper.wrapper(glMultiTexCoord2dv).setInputArraySize(
    'v', 2
)
glMultiTexCoord2fv=wrapper.wrapper(glMultiTexCoord2fv).setInputArraySize(
    'v', 2
)
glMultiTexCoord2iv=wrapper.wrapper(glMultiTexCoord2iv).setInputArraySize(
    'v', 2
)
glMultiTexCoord2sv=wrapper.wrapper(glMultiTexCoord2sv).setInputArraySize(
    'v', 2
)
glMultiTexCoord3dv=wrapper.wrapper(glMultiTexCoord3dv).setInputArraySize(
    'v', 3
)
glMultiTexCoord3fv=wrapper.wrapper(glMultiTexCoord3fv).setInputArraySize(
    'v', 3
)
glMultiTexCoord3iv=wrapper.wrapper(glMultiTexCoord3iv).setInputArraySize(
    'v', 3
)
glMultiTexCoord3sv=wrapper.wrapper(glMultiTexCoord3sv).setInputArraySize(
    'v', 3
)
glMultiTexCoord4dv=wrapper.wrapper(glMultiTexCoord4dv).setInputArraySize(
    'v', 4
)
glMultiTexCoord4fv=wrapper.wrapper(glMultiTexCoord4fv).setInputArraySize(
    'v', 4
)
glMultiTexCoord4iv=wrapper.wrapper(glMultiTexCoord4iv).setInputArraySize(
    'v', 4
)
glMultiTexCoord4sv=wrapper.wrapper(glMultiTexCoord4sv).setInputArraySize(
    'v', 4
)
glLoadTransposeMatrixf=wrapper.wrapper(glLoadTransposeMatrixf).setInputArraySize(
    'm', 16
)
glLoadTransposeMatrixd=wrapper.wrapper(glLoadTransposeMatrixd).setInputArraySize(
    'm', 16
)
glMultTransposeMatrixf=wrapper.wrapper(glMultTransposeMatrixf).setInputArraySize(
    'm', 16
)
glMultTransposeMatrixd=wrapper.wrapper(glMultTransposeMatrixd).setInputArraySize(
    'm', 16
)
### END AUTOGENERATED SECTION
GL_SRC0_ALPHA = GL_SOURCE0_ALPHA # alias
GL_SRC0_RGB = GL_SOURCE0_RGB # alias
GL_SRC1_ALPHA = GL_SOURCE1_ALPHA # alias
GL_SRC1_RGB = GL_SOURCE1_RGB # alias
GL_SRC2_ALPHA = GL_SOURCE2_ALPHA # alias
GL_SRC2_RGB = GL_SOURCE2_RGB # alias

from OpenGL import wrapper
from OpenGL.raw.GL.VERSION import GL_1_3 as _simple
from OpenGL.GL import images, glget

for dimensions in (1,2,3):
    for function in ('glCompressedTexImage%sD','glCompressedTexSubImage%sD'):
        name = function%(dimensions,)
        globals()[ name ] = images.compressedImageFunction(
            getattr( _simple, name )
        )
        try:
            del name, function
        except NameError as err:
            pass
    try:
        del dimensions
    except NameError as err:
        pass

if _simple.glGetCompressedTexImage:
    def glGetCompressedTexImage( target, level, img=None ):
        """Retrieve a compressed texture image"""
        if img is None:
            length = glget.glGetTexLevelParameteriv(
                target, 0,
                _simple.GL_TEXTURE_COMPRESSED_IMAGE_SIZE_ARB,
            )
            img = arrays.ArrayDataType.zeros( (length,), constants.GL_UNSIGNED_BYTE )
        return _simple.glGetCompressedTexImage(target, 0, img);
