from GLAPP import GLAPP
from OpenGL import GL
from array import array
import ctypes
import glm
import math

class SphereApp(GLAPP):

    def setup(self):
        # Window setup
        self.title("Dotted Sphere")
        self.size(800,800)

        # OpenGL Initialization
        GL.glClearColor(0.2, 0.2, 0.2, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        # Pipeline (shaders)
        self.pipeline = self.loadPipeline("SimplePipeline")
        GL.glUseProgram(self.pipeline)
        self.a = 0
        self.sphereArrayBufferId = None

    def map(self,valor, v0, vf, m0, mf):
        return m0+(((valor-v0)*(mf-m0))/(vf-v0))


    def coordenadaEsferica(self,i,j, N = 50,r = 1):
        theta = self.map(i,0,N,-math.pi/2,math.pi/2)
        phy = self.map(j,0,N,0,2*math.pi)
        x = r * math.cos(theta)*math.cos(phy)
        y = r * math.sin(theta)
        z = r * math.cos(theta)*math.sin(phy)
        return x, y, z

    def drawSphere(self):
        n = 50
        N = 50
        if self.sphereArrayBufferId == None:
            position = array('f')
            for i in range(0,N):
                
                for j in range(0,N):
                    x,y,z = self.coordenadaEsferica(i,j)

                    position.append(x)
                    position.append(y)
                    position.append(z)

                    a,b,c = self.coordenadaEsferica(i + 1,j)

                    position.append(a)
                    position.append(b)
                    position.append(c)


                    a,b,c = self.coordenadaEsferica(i + 1,j + 1)

                    position.append(a)
                    position.append(b)
                    position.append(c)

                    a,b,c = self.coordenadaEsferica(i + 1,j + 1)

                    position.append(a)
                    position.append(b)
                    position.append(c)


                    a,b,c = self.coordenadaEsferica(i,j + 1)

                    position.append(a)
                    position.append(b)
                    position.append(c)

                    x,y,z = self.coordenadaEsferica(i,j)

                    position.append(x)
                    position.append(y)
                    position.append(z)





                  
                    print(len(position))

            self.sphereArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.sphereArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize, ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idColorBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idColorBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize, ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
        
        
        GL.glBindVertexArray(self.sphereArrayBufferId)
        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,100)
        camera = glm.lookAt(glm.vec3(0,0,5),glm.vec3(0),glm.vec3(0,1,0))
        #model = glm.rotate(self.a,glm.vec3(0,0,0.01)) * glm.rotate(self.a,glm.vec3(0,0.01,0)) * glm.rotate(self.a,glm.vec3(0.01,0,0)) 

        model = glm.rotate(self.a,glm.vec3(0,0,0.1))

        #model = glm.rotate(self.a,glm.vec3(0,0,0.01)) 
        mvp = projection * model * camera 
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        GL.glDrawArrays(GL.GL_TRIANGLES,0,n * n * 6)
        self.a += 0.01

    def draw(self):
        # clear screen and depth buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        # Draw a Dotted Sphere
        self.drawSphere()

SphereApp()
