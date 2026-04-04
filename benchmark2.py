import timeit

cmdline = [
    "C:\\Riot Games\\League of Legends\\LeagueClientUx.exe",
    "--riotclient-auth-token=some_token",
    "--riotclient-app-port=50000",
    "--no-rads",
    "--disable-self-update",
    "--region=NA",
    "--locale=en_US",
    "--remoting-auth-token=abcd1234efgh5678",
    "--respawn-command=LeagueClient.exe",
    "--respawn-display-name=League of Legends",
    "--app-port=50001",
    "--install-directory=C:\\Riot Games\\League of Legends",
    "--app-name=LeagueClient",
    "--ux-name=LeagueClientUx",
    "--ux-state=Starting"
] * 10

def old_way():
    port = None
    auth_token = None
    for arg in cmdline:
        if "--app-port=" in arg:
            port = arg.split("=")[1]
        if "--remoting-auth-token=" in arg:
            auth_token = arg.split("=")[1]
    return port, auth_token

def generator_way():
    port = next((arg.split("=", 1)[1] for arg in cmdline if arg.startswith("--app-port=")), None)
    auth_token = next((arg.split("=", 1)[1] for arg in cmdline if arg.startswith("--remoting-auth-token=")), None)
    return port, auth_token

def break_way():
    port = None
    auth_token = None
    for arg in cmdline:
        if arg.startswith("--app-port="):
            port = arg.split("=", 1)[1]
        elif arg.startswith("--remoting-auth-token="):
            auth_token = arg.split("=", 1)[1]
        if port and auth_token:
            break
    return port, auth_token

print("Old way:", timeit.timeit(old_way, number=100000))
print("Generator way:", timeit.timeit(generator_way, number=100000))
print("Break way:", timeit.timeit(break_way, number=100000))
