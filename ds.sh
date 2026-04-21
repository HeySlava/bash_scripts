#!/bin/bash

declare -A SERVICES
SERVICES=(
    ["torrent"]="$HOME/code/torrent"
    ["jellyfin"]="$HOME/code/jellyfin"
    ["pomodoro"]="$HOME/code/pomodoro"
    ["postgres"]="$HOME/code/postgres"
    ["ch-local"]="$HOME/code/clickhouse-local"
    ["ch-stepic"]="$HOME/code/clickhouse-stepic"
    ["minio"]="$HOME/code/minio"
    ["yac"]="$HOME/code/stat-yac"
)

function ds() {
    local cmd=$1
    local service=$2

    if [[ -z "$cmd" ]]; then
        echo "Usage: ds [up|down|restart|logs|ps|ls] [service]"
        return 1
    fi

    if [[ "$cmd" == "ls" ]]; then
        printf "%-15s %-45s %s\n" "SERVICE" "PATH" "STATUS"
        printf "%-15s %-45s %s\n" "-------" "----" "------"
        for name in "${!SERVICES[@]}"; do
            local path="${SERVICES[$name]}"
            local status="OFF"

            local f=""
            [[ -f "$path/docker-compose.yml" ]] && f="$path/docker-compose.yml"
            [[ -f "$path/docker-compose.yaml" ]] && f="$path/docker-compose.yaml"

            if [[ -n "$f" ]]; then
                if [ -n "$(docker compose -f "$f" ps --filter "status=running" -q 2>/dev/null)" ]; then
                    status="RUNNING"
                fi
            fi
            printf "%-15s %-45s %s\n" "$name" "$path" "$status"
        done | sort
        return 0
    fi

    if [[ "$cmd" == "ps" ]]; then
        for path in "${SERVICES[@]}"; do
            if [[ -d "$path" ]]; then
                local f=""
                [[ -f "$path/docker-compose.yml" ]] && f="$path/docker-compose.yml"
                [[ -f "$path/docker-compose.yaml" ]] && f="$path/docker-compose.yaml"
                if [[ -n "$f" ]]; then
                    docker compose -f "$f" ps
                fi
            fi
        done
        return 0
    fi

    if [[ -z "$service" ]]; then
        echo "Error: Service name required"
        return 1
    fi

    local service_path="${SERVICES[$service]}"

    if [[ -z "$service_path" ]]; then
        echo "Error: Service '$service' is not defined in ds.sh"
        return 1
    fi

    if [[ ! -d "$service_path" ]]; then
        echo "Error: Directory not found: $service_path"
        return 1
    fi

    local compose_file=""
    if [[ -f "$service_path/docker-compose.yml" ]]; then
        compose_file="$service_path/docker-compose.yml"
    elif [[ -f "$service_path/docker-compose.yaml" ]]; then
        compose_file="$service_path/docker-compose.yaml"
    fi

    if [[ -z "$compose_file" ]]; then
        echo "Error: No docker-compose.yml or .yaml found in $service_path"
        return 1
    fi

    case "$cmd" in
        up)
            docker compose -f "$compose_file" up --build -d
            ;;
        down)
            docker compose -f "$compose_file" down
            ;;
        restart)
            docker compose -f "$compose_file" restart
            ;;
        logs)
            docker compose -f "$compose_file" logs -f --tail=100
            ;;
        *)
            echo "Unknown command: $cmd"
            echo "Available: up, down, restart, logs, ps, ls"
            return 1
            ;;
    esac
}

_ds_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    local commands="up down restart logs ps ls"
    if [[ ${COMP_CWORD} -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
        return 0
    fi
    if [[ ${COMP_CWORD} -eq 2 ]]; then
        local service_names="${!SERVICES[@]}"
        COMPREPLY=( $(compgen -W "${service_names}" -- ${cur}) )
        return 0
    fi
}

complete -F _ds_completion ds
