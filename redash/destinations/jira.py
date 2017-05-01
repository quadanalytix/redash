import json
import logging
import requests
import os

from restkit import Resource, BasicAuth

from redash.destinations import *

class Jira(BaseDestination):

    @classmethod
    def configuration_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'project_name': {
                    'type': 'string',
                    'title': 'Project Name'
                },
                'summary': {
                    'type': 'string',
                    'title': 'Summary'
                },
                'description': {
                    'type': 'string',
                    'title': 'Description'
                },
                'priority': {
                    'type': 'string',
                    'title': 'Priority'
                }
            }
        }

    @classmethod
    def icon(cls):
        return 'fa-jira'

    def notify(self, alert, query, user, new_state, app, host, options):

        username = os.environ.get('USERNAME','')
        password = os.environ.get('PASSWORD','')

        auth = BasicAuth(username, password)

        server_url = "https://quadanalytix.atlassian.net"
        resource_name = "issue"
        complete_url = "%s/rest/api/latest/%s/" % (server_url, resource_name)
        resource = Resource(complete_url, filters=[auth])
        #create payload for JIRA

        if options.get('project_name'): project = options.get('project_name')
        if options.get('summary'): summary = options.get('summary')
        if options.get('description'): description = options.get('description')
        if options.get('priority'): priority = options.get('priority')

        data = {
            "fields": {
                "project": {
                    "key": project
                },
                "summary": summary,
                "description": description,
                "issuetype": {
                    "name": "Bug"
                },
                "priority": {
                    "name": priority
                }
            }
        }

        try:
            response = resource.post(headers={'Content-Type': 'application/json'}, payload=json.dumps(data))
            logging.warning(response.text)
            if response.status_code != 200:
                logging.error("JIRA send ERROR. status_code => {status}".format(status=response.status_code))
        except Exception:
            logging.exception("JIRA send ERROR.")

register(Jira)
