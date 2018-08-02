import subprocess
import docker
import json
import time

# docker_client = docker.from_env()
docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
docker_stat_json ="\"{container_id:{{ .Container }},raw_mem:{{ .MemUsage }},percent_mem:{{ .MemPerc }},net_io:{{ .NetIO }},block_io:{{ .BlockIO }},cpu:{{ .CPUPerc }},name:{{.Name}}}\""


# Sends the actual results back to the caller in json form
# Doesnot include container specific calculations
def get_docker_stats_api():
    global docker_client
    for client in docker_client.containers():
        # stats is a generator object generates result every 1 second
        stats = docker_client.stats(client['Id'], stream=False)
        print(json.dumps(stats))


# Format the string from `docker stats` and returns results as dictionaries
def format_string(info_string: str, extra_information: dict = {}):
    container_dict = {}
    information = info_string.split(',')
    container_dict["container_id"] = information[0].split(':')[1]
    container_dict["raw_memory"] = information[1].split(':')[1]
    container_dict["percent_memory"] = information[2].split(':')[1]
    container_dict["net_io"] = information[3].split(':')[1]
    container_dict["block_io"] = information[4].split(':')[1]
    container_dict["cpu_percent"] = information[5].split(':')[1]
    container_dict["cont_name"] = information[6].split(':')[1].replace('}', '')
    if extra_information:
        for key, value in extra_information.items():
            container_dict[key] = value
    return container_dict


# Get the docker stats from non api call. First gets stats for all docker containers, then formats them
def get_docker_stats_nonapi():
    global docker_client 
    global docker_stat_json
    formatted_string = []
    raw_string = subprocess.run("""docker stats --no-stream """+"--format " +
                                    docker_stat_json, check=True, stdout=subprocess.PIPE, shell=True).stdout
    container_stats = raw_string.decode('utf-8').strip().split('\n')
    for container_stat in container_stats:
        formatted_string.append(format_string(container_stat))
    return formatted_string





# if __name__=="__main__":
#     print([client['Id'] for client in docker_client.containers()])
#     print(docker_client.stats)
#     start = time.time()
#     result = get_docker_stats_nonapi()
#     print(result)
#     print("Ended at {}".format(time.time() -start))
