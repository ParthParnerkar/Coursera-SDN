'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
	'''
	fanout: number of lower level elements attached to each element
	linkopts1: options for top level links (core-aggregation)
	linkopts2: options for aggregation-edge links
	linkopts3: options for edge-host links
	'''
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
	agCount = 1
	edgeCount = 1
	hostCount = 1
	coreSwitch = self.addSwitch('c1')
	for i1 in range(fanout):
		switch = self.addSwitch('a%s' % agCount)
		agCount += 1
		self.addLink(switch, coreSwitch, **linkopts1);
		for l2 in range(fanout):
			eSwitch = self.addSwitch('e%s'%edgeCount)
			edgeCount += 1
			self.addLink(eSwitch, switch, **linkopts2);
			for l3 in range(fanout):
				host = self.addHost('h%s'%hostCount)
				hostCount += 1
				self.addLink(host,eSwitch, **linkopts3); 
        
                    
topos = { 'custom': ( lambda: CustomTopo({'bw':10,'delay':'1ms'},{'bw':8,'delay':'2ms'},{'bw':4,'delay':'4ms'},fanout=2) ) }

def simpleTest():
   "Create and test a simple network"
   topo = CustomTopo({'bw':10,'delay':'1ms'},{'bw':8,'delay':'2ms'},{'bw':4,'delay':'4ms'},fanout=2)
   net = Mininet(topo)
   net.start()
   print "Dumping host connections"
   dumpNodeConnections(net.hosts)
   print "Testing network connectivity"
   net.pingAll()
   net.stop()

if __name__ == '__main__':
   # Tell mininet to print useful information
   setLogLevel('info')
   simpleTest()

