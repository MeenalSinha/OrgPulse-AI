"""
Central registry of all MCP connectors. The integrations router and Slack
app both read from this single source of truth, so adding a new connector
means adding one class + one line here.
"""
from .github_connector import GitHubConnector
from .jira_connector import JiraConnector
from .notion_connector import NotionConnector
from .confluence_connector import ConfluenceConnector
from .gdrive_connector import GoogleDriveConnector
from .slack_connector import SlackConnector
from .calendar_connector import GoogleCalendarConnector
from .linear_connector import LinearConnector
from .figma_connector import FigmaConnector
from .gitlab_connector import GitLabConnector
from .azure_devops_connector import AzureDevOpsConnector

CONNECTOR_REGISTRY = {
    "github": GitHubConnector(),
    "jira": JiraConnector(),
    "notion": NotionConnector(),
    "confluence": ConfluenceConnector(),
    "gdrive": GoogleDriveConnector(),
    "slack": SlackConnector(),
    "calendar": GoogleCalendarConnector(),
    "linear": LinearConnector(),
    "figma": FigmaConnector(),
    "gitlab": GitLabConnector(),
    "azure_devops": AzureDevOpsConnector(),
}
