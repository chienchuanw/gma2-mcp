import dotenv
import telnetlib
import time

GMA_HOST = dotenv.get_key(".env", "GMA_HOST")
# grandMA2 uses 30000 as default, 30001 for read-only
GMA_PORT = 30000
GMA_USER = dotenv.get_key(".env", "GMA_USER") or "administrator"
GMA_PASSWORD = dotenv.get_key(".env", "GMA_PASSWORD") or "admin"


def login():
    """Login to grandMA2."""
    tn = None

    try:
        # Setup telnet connection
        tn = telnetlib.Telnet(GMA_HOST, GMA_PORT)

        time.sleep(1)

        # Read initial message
        init_res = tn.read_very_eager()
        print("=== initial message ===")
        print(init_res.decode("utf-8"))
        print("=== initial message end ===\n")

        login_cmd = f'login "{GMA_USER}" "{GMA_PASSWORD}"\r\n'

        tn.write(login_cmd.encode("utf-8"))

        time.sleep(0.5)

        login_res = tn.read_very_eager()
        print("=== login response ===")
        print(login_res.decode("utf-8"))
        print("=== login response end ===")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if tn is not None:
            tn.close()


def main():
    print("Hello from gma2-mcp!")
    print(f"Connecting to {GMA_HOST}:{GMA_PORT} as {GMA_USER}...")
    login()


if __name__ == "__main__":
    main()
