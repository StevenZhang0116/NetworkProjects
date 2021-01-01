import socket
import traceback

server_name='steven_server'
server_ip='127.0.0.1'
server_port=8080

access_counter=0

def start_server():
	'''
	'''

	print(f'start server on {server_ip}({server_port})')

	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.bind((server_ip,server_port))
	sock.listen(1)

	try:

		while True:
			print(f'await client request.')
			conn,addr=sock.accept()
			handle_request(conn,addr)
			conn.close()
	except Exception as ex:
		traceback.print_exc()
		print('[error]:start_server.')		

	sock.close()


def handle_request(conn,addr):
	'''
	'''
	print(f'handle request from ({addr})')

	buf=conn.recv(1024)
	req=HttpRequest(buf)

	# print("<BUFFER>")
	# print(buf)

	print(f'<-- request -->')
	print(f'{req}')
	print(f'--> request end <---')

	rh=ReqHandler()
	resp=rh.handle(req)

	sval=resp.build()

	print(f'<-- response -->')
	print(f'{sval}')
	print(f'--> response end <--')

	conn.send(str.encode(sval))

	print(f'handle done.')
	return

class ReqHandler:
	'''
	'''
	def __init__(self):
		'''
		'''
		self.resp=HttpResponse()
		return

	def handle(self,req):
		'''
		'''
		if req.isGET():
			self.handle_get(req)
		else:
			self.resp.setError()

		return self.resp

	def handle_get(self,req):
		'''
		'''
		path=req.path

		if path=='/':
			self.handle_root(req)
		elif path=='/page2':
			self.handle_page2(req)
		elif path=='/page3':
			self.handle_page3(req)
		else:
			self.resp.setNotFound()

		return

	def handle_root(self,req):
		'''
		'''
	
		global access_counter
		access_counter+=1

		html=f'''
<HTML>
<HEAD>
	<TITLE>HTTP Homework</TITLE>
</HEAD>
<BODY>
	<H3><CENTER>HTTP Homework</CENTER></H3>
	This is the main page
	<P>
		You can click on <A HREF="/page2">page 2</A> or <A HREF="/page3">Page 3</A>
	<P>
	<CENTER>This server has been used {access_counter} times</CENTER>
</BODY>
</HTML>		
		'''
		self.resp.data=html

		return

	def handle_page2(self,req):
		'''
		'''

		global access_counter
		access_counter+=1

		html=f'''
<HTML>
<HEAD>
	<TITLE>HTTP Homework</TITLE>
</HEAD>
<BODY>
	<H3><CENTER>HTTP Homework</CENTER></H3>
	This is page 2
	<P>
		You can go <A HREF="/">back</A> 
	<P>
	<CENTER>This server has been used {access_counter} times</CENTER>
</BODY>
</HTML>		
		'''

		self.resp.data=html

		return

	def handle_page3(self,req):
		'''
		'''

		global access_counter
		access_counter+=1

		html=f'''
<HTML>
<HEAD>
	<TITLE>HTTP Homework</TITLE>
</HEAD>
<BODY>
	<H3><CENTER>HTTP Homework</CENTER></H3>
	This is page 3
	<P>
		You can go <A HREF="/">back</A> 
	<P>
	<CENTER>This server has been used {access_counter} times</CENTER>
</BODY>
</HTML>		
		'''

		self.resp.data=html

		return


class HttpResponse:
	'''
	'''
	def __init__(self):
		'''
		'''
		self.version='HTTP/1.0'
		self.status_code=200
		self.status_desc='OK'
		self.server= " NETID: ZZ2589"
		self.contentType='text/html'
		self.connection='Closed'
		self.data=None

		return

	def setStatus(self,code,desc):
		'''
		'''
		self.status_code=code
		self.status_desc=desc
		return

	def setOK(self):
		'''
		'''
		self.status_code=200
		self.status_desc='OK'
		return

	def setNotFound(self):
		'''
		'''
		self.status_code=404
		self.status_desc='Not Found'
		return

	def setError(self):
		'''
		'''
		self.status_code=400
		self.status_desc='Bad Request'

		return

	def build(self):
		'''
		'''
		ret=True

		sval=f'{self.version} {self.status_code} {self.status_desc}\r\n'
		if self.server is not None:
			sval+=f'Server:{self.server}\r\n'

		clen=0
		if self.data is not None:
			clen=len(self.data)

		sval+=f'Content-Length:{clen}\r\n'

		sval+=f'Content-Type:{self.contentType}\r\n'
		sval+=f'Connection:{self.connection}\r\n'

		sval+='\r\n'

		if clen>0:
			sval+=self.data

		ret=sval

		return ret

class HttpRequest:
	'''
	'''
	def __init__(self,buf):
		'''
		'''
		sbuf=None
		if isinstance(buf,bytes):
			sbuf=bytes.decode(buf)
		else:
			sbuf=buf

		self.method=None
		self.path=None
		self.version=None
		self._header={}

		self._parse(sbuf)

		return

	def isGET(self):
		'''
		'''
		ret=False
		if self.method is not None:
			if self.method.upper()=='GET':
				ret=True

		return ret

	def header(self,name):
		'''
		'''
		ret=None
		ret=self._header.get(name)
		return ret

	def __repr__(self):
		'''
		'''
		ret=f'HttpRequest(method:({self.method}))\n'
		ret+=f'\tpath({self.path})\n'
		ret+=f'\tversion({self.version})\n'
		ret+=f'header:[{len(self._header)}]\n'
		for k,v in self._header.items():
			ret+=f'\t{k}=[{v}]\n'

		return ret

	def _parse(self,sbuf):
		'''
		'''
		a=sbuf.split('\n')
		line=a[0].strip()
		self._parse_status(line)

		for i in range(1,len(a)):
			line=a[i].strip()
			self._parse_header(line)

		return

	def _parse_status(self,line):
		'''
		'''
		a=line.split(' ')
		self.method=a[0]
		self.path=a[1]
		self.version=a[2]
		return

	def _parse_header(self,line):
		'''
		'''
		pos=line.find(':')
		name=line[0:pos].strip()
		val=line[pos+1:].strip()

		if len(name)>0:
			self._header[name]=val

		return

def main_routine():
	'''
	'''
	print(f'begin.')

	try:
		start_server()
	except Exception as ex:
		traceback.print_exc()
		print(f'[error]:({ex})')

	print(f'end.')

	return


if __name__=='__main__':
	main_routine()


