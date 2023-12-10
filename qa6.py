import subprocess
import json

server_ip = "192.168.4.151"


def client(server_ip):
    try:
        command = f"iperf3 -c {server_ip} -J"
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        result, error = process.communicate()

        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode, command, output=result
            )

        return result, error
    except subprocess.CalledProcessError as e:
        error_output = json.loads(e.output)
        error_message = error_output.get("error", str(error_output))
        print(
            f"Error executing iperf command. Return code: {e.returncode}. Error cause: {error_message}"
        )
        return None, None


def parser(output):
    json_data = json.loads(output)
    result_list = json_data["intervals"]
    return result_list


if __name__ == "__main__":
    result, error = client(server_ip)

    if result:
        result_list = parser(result)
        for interval in result_list:
            transfer = round(interval["sum"]["bytes"] / 1e6, 2)
            bitrate = round(interval["sum"]["bits_per_second"] / 1e9, 2)
            retr = interval["sum"]["retransmits"]
            cwnd = round(interval["streams"][0]["snd_cwnd"] / 1e6, 2)
            if transfer > 2:
                print(
                    f"Interval: {interval['sum']['start']}-{interval['sum']['end']}, Transfer: {transfer} Mbytes, Bitrate: {bitrate} Gbits/s, Retr: {retr}, Cwnd: {cwnd} MBytes"
                )

