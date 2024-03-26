import firewall
import Azure_access

def main():
    Azure_access.run()
    firewall.run()

if __name__ == "__main__":
    main()