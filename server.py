import random

import requests
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool

# Create server
mcp = FastMCP("Echo Server")

flexApi = "https://jeremydev.flexrentalsolutions.com/f5/api"



@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"[debug-server] add({a}, {b})")
    return a + b


@mcp.tool()
def get_secret_word() -> str:
    print("[debug-server] get_secret_word()")
    return random.choice(["apple", "banana", "cherry"])


@mcp.tool()
def get_current_weather(city: str) -> str:
    print(f"[debug-server] get_current_weather({city})")

    endpoint = "https://wttr.in"
    response = requests.get(f"{endpoint}/{city}")
    return response.text

@mcp.tool(description='Get the location identities for this business, returning Id/Name pairs.')
def getBusinessLocations() -> str:
    print(f"[getting business locations]")

    response = requests.get(url=f"{flexApi}/business-location/identity", headers={"X-Auth-Token": "iU6nihZrQax5RYkmncY8BHgJ4XohzQtFSptq"})
    return response.text

@mcp.tool(description='Get the location details for a specific location, provided that location\'s id.')
def getBusinessLocationDetails(id: str) -> str:
    print(f"[getting business locations]")

    response = requests.get(url=f"{flexApi}/business-location/{id}", headers={"X-Auth-Token": "iU6nihZrQax5RYkmncY8BHgJ4XohzQtFSptq"})
    return response.text

@mcp.tool(description='Get the element definition identities  for this business, returning ID/name pairs')
def getElementDefinitions() -> str:
    print(f"[getting element definitions]")

    response = requests.get(url=f"{flexApi}/element-definition/identity", headers={"X-Auth-Token": "iU6nihZrQax5RYkmncY8BHgJ4XohzQtFSptq"})
    return response.text

@mcp.tool(description='create a project element. Requires an elementDefinitionId, name, plannedStartDate, plannedEndDate.')
def createElement(elementDefinitionId: str, name: str, plannedStartDate: str, plannedEndDate: str) -> str:
    print(f"[getting business locations]")

    response = requests.post(url=f"{flexApi}/element", data={"definitionId": elementDefinitionId, "name": name, "plannedStartDate": plannedStartDate, "plannedEndDate": plannedEndDate }, headers={"X-Auth-Token": "iU6nihZrQax5RYkmncY8BHgJ4XohzQtFSptq"})
    return response.text

if __name__ == "__main__":
    mcp.run(transport="sse")