from GLAPP import GLAPP
from OpenGL import GL
from array import array
import glm
import math
import ctypes

class OctaedroWithTextureApp(GLAPP):

    def setup(self):
        # Window setup
        self.title("Octaedro With Texture")
        self.size(1100,1100)

        # OpenGL Initialization
        GL.glClearColor(0.2, 0.2, 0.2, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        # Pipeline (shaders)
        pipeline = self.loadPipeline("SimpleTexture")
        GL.glUseProgram(pipeline)
        self.a = 0
        self.OctaedroArrayBufferId = None

    def drawOctaedro(self):
        if self.OctaedroArrayBufferId == None:
            position = array('f',[
                 1.0, 0.0, 0.0,
                 0.0, 0.0, 1.0,
                 -1.0, 0.0, 0.0,
                 0.0, 0.0, -1.0,
                 0.0, 1.0, 0.0,
                 0.0, -1.0, 0.0,
            ])

            textureCoord = array('f',[
                 1.0, 0.0, 0.0,
                 0.8, 0.0, 0.0,
                 0.6, 0.0, 0.0,
                 0.4, 0.0, 0.0,
                 0.0, 1.0, 0.0,
                 0.0, 0.8, 0.0,
                 0.0, 0.6, 0.0,
                 0.0, 0.4, 0.0,
            ])

            self.OctaedroArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.OctaedroArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize, ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idTextureBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idTextureBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(textureCoord)*textureCoord.itemsize, ctypes.c_void_p(textureCoord.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
        
        GL.glBindVertexArray(self.OctaedroArrayBufferId)
        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,100)
        camera = glm.lookAt(glm.vec3(0,0,5),glm.vec3(0),glm.vec3(0,1,0))
        model = glm.rotate(self.a,glm.vec3(0,0,1)) * glm.rotate(self.a,glm.vec3(0,1,0)) * glm.rotate(self.a,glm.vec3(1,0,0)) 
        mvp = projection * camera * model
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        GL.glDrawArrays(GL.GL_TRIANGLES,0,160)
        self.a += 0.001


    def draw(self):
        # clear screen and depth buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        # Draw a Triangle
        self.drawOctaedro()

OctaedroWithTextureApp()
