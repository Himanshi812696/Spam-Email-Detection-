import socket
import sys

def test_connection(host, port):
    """Test if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✓ Port {port} on {host} is OPEN and listening")
            return True
        else:
            print(f"✗ Port {port} on {host} is CLOSED or refused")
            return False
    except Exception as e:
        print(f"✗ Error testing connection: {e}")
        return False

if __name__ == "__main__":
    print("Testing Flask connection...")
    test_connection("127.0.0.1", 10000)
    test_connection("localhost", 10000)
