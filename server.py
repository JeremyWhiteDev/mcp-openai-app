import os
import random

from dotenv import load_dotenv
import pytz
import requests
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool

from dateutil import parser
from datetime import datetime

# Create server
mcp = FastMCP("Echo Server")

load_dotenv()
flexApiKey = os.getenv('FLEX_API_KEY')
flexApi = os.getenv('FLEX_API_URL')

@mcp.tool(description=(
        "Get all the business locations . "
        "Use this when a user asks about business locations or needs to provide a business location"
    ))
def getBusinessLocations() -> str:
    print(f"[getting business locations]")

    response = requests.get(url=f"{flexApi}/business-location/identity", headers={"X-Auth-Token": flexApiKey})
    return response.text

@mcp.tool(description='Get the location details for a specific location, provided that location\'s id.')
def getBusinessLocationDetails(id: str) -> str:
    print(f"[getting business locations]")

    response = requests.get(url=f"{flexApi}/business-location/{id}", headers={"X-Auth-Token": flexApiKey})
    return response.text

@mcp.tool(description=(
        "Get all element definitions (like Quote, Project, Event). "
        "Use this to find the ID of an element type when the user asks to create one."
        "Use this to find a list of element definitions or element types if the user asks for it."
    ))
def getElementDefinitions() -> str:
    print(f"[getting element definitions]")

    response = requests.get(url=f"{flexApi}/element-definition/identity", headers={"X-Auth-Token": flexApiKey})
    return response.text

# TODO
# i'd need a date parser or something

@mcp.tool(description=(
        "Create a new event element. "
        "Use this when a user requests to create a quote, project, or event."
        "You must provide the element definition ID (use getElementDefinitions to look it up), "
        "a business location ID (use getBusinessLocations to look it up), "
        "a name for the element, and the planned start and end dates. "
        "Do not ask for additional fields"
    ))
def createElement(elementDefinitionId: str, businessLocationId: str, name: str, plannedStartDate: str, plannedEndDate: str, ) -> str:
    print(f"[creating a new element elementDefId: {elementDefinitionId}, bizLoc: {businessLocationId}, start: {plannedStartDate} end: {plannedEndDate}]")

    parsedStart = parser.parse(plannedStartDate)
        # Optional: ensure it's timezone-aware (UTC)
    if parsedStart.tzinfo is None:
        parsedStart = parsedStart.replace(tzinfo=pytz.UTC)

    parsedStart = parsedStart.isoformat()

    parsedEnd = parser.parse(plannedEndDate)
        # Optional: ensure it's timezone-aware (UTC)
    if parsedEnd.tzinfo is None:
        parsedEnd = parsedEnd.replace(tzinfo=pytz.UTC)

    parsedEnd = parsedEnd.isoformat()

    print(f"[parsed start/end dates: {parsedStart} end: {parsedEnd}]")


    response = requests.post(url=f"{flexApi}/element", json={"definitionId": elementDefinitionId, "locationId": businessLocationId, "currencyId": "911e3d4c-aedc-11df-b8d5-00e08175e43e", "name": name, "plannedStartDate": plannedStartDate, "plannedEndDate": plannedEndDate }, headers={"X-Auth-Token": "iU6nihZrQax5RYkmncY8BHgJ4XohzQtFSptq"})
    return response.text


@mcp.tool(description=(
        "search for resources"
        "use this when needing to find a resourceId for a provided resource name"
        "the searchTerm should be a partial name for the inventory model"
        "if provided a plural, use a singular"
    ))
def searchResource(searchTerm: str) -> str:
    print(f"[searching resources {searchTerm}]")
    response = requests.get(url=f"{flexApi}/inventory-model/search-api", params={"searchText": searchTerm}, headers={"X-Auth-Token": flexApiKey})

    print(f"[searching result >>>>>> {response.text}]")
    return response.text

@mcp.tool(description=(
        "add resource line item to a specific event element"
        "You must provide the element ID "
        "and the resource ID of the item being added (if the element), "
        "as well as the qty. If the qty isn't specified by the user, assume 1"
        "example usage: Create a quote with 5 widgets on it. Create the quote, then Look up widget ID using searchResource, then add resource line item"
    ))
def addResourceLineItem(elementId: str, resourceId: str, qty: int) -> str:
    print(f"[add resourceLine to an new element: {elementId} resourceId {resourceId}]")

    response = requests.post(url=f"{flexApi}/line-item/{elementId}/add-resource/{resourceId}", params={"managedResourceLineItemType": "inventory-model", "quantity": qty, "resourceParentId": ""},  headers={"X-Auth-Token": flexApiKey})
    return response.text

if __name__ == "__main__":
    mcp.run(transport="sse")