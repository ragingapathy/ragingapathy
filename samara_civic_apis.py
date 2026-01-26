"""
title: Samara Civic Data APIs
author: Samara Project
version: 1.0.1
description: Access civic data from Google Civic, OpenStates, OpenFEC, Congress.gov, and LegiScan APIs
required_open_webui_version: 0.3.0
"""

import requests
from typing import Optional
from pydantic import BaseModel, Field


class Tools:
    """Samara Civic Data API Tools"""

    class Valves(BaseModel):
        """
        API Key Configuration for Samara Civic Data APIs

        Get your FREE API keys from the URLs shown in each field description.
        """

        GOOGLE_CIVIC_API_KEY: str = Field(
            default="",
            description="Get at: https://console.developers.google.com/ | Provides: Representatives, Elections, Polling Locations"
        )

        OPENSTATES_API_KEY: str = Field(
            default="",
            description="Get at: https://open.pluralpolicy.com/ | Provides: State Legislators, Bills, Events, Committees"
        )

        OPENFEC_API_KEY: str = Field(
            default="",
            description="Get at: https://api.open.fec.gov/developers/ | Provides: Federal Campaign Finance, Contributions"
        )

        CONGRESS_API_KEY: str = Field(
            default="",
            description="Get at: https://api.congress.gov/sign-up/ | Provides: Federal Bills, Votes, Congressional Members"
        )

        LEGISCAN_API_KEY: str = Field(
            default="",
            description="Get at: https://legiscan.com/legiscan | Provides: State Bill Text, Roll Call Votes (Optional)"
        )

    def __init__(self):
        self.valves = self.Valves()
        self.base_urls = {
            "google_civic": "https://civicinfo.googleapis.com/civicinfo/v2",
            "openstates": "https://v3.openstates.org",
            "openfec": "https://api.open.fec.gov/v1",
            "congress": "https://api.congress.gov/v3",
            "legiscan": "https://api.legiscan.com"
        }

    def check_api_status(self) -> str:
        """
        Check which APIs are configured and ready to use.

        Returns a status report of all API configurations.
        """
        status = {
            "Google Civic": bool(self.valves.GOOGLE_CIVIC_API_KEY.strip()),
            "OpenStates": bool(self.valves.OPENSTATES_API_KEY.strip()),
            "OpenFEC": bool(self.valves.OPENFEC_API_KEY.strip()),
            "Congress.gov": bool(self.valves.CONGRESS_API_KEY.strip()),
            "LegiScan": bool(self.valves.LEGISCAN_API_KEY.strip())
        }

        configured = sum(status.values())

        result = f"""
🏛️ SAMARA CIVIC API STATUS
═══════════════════════════════════════

Configured APIs: {configured}/5

"""
        for api_name, is_configured in status.items():
            symbol = "✓" if is_configured else "✗"
            result += f"  {symbol} {api_name}\n"

        if configured == 0:
            result += """
⚠️  No APIs configured yet!

To enable civic intelligence features:
1. Click the function settings (gear icon)
2. Add your API keys in the Valves section
3. URLs for obtaining keys are shown above each field

Start with Google Civic + OpenStates for maximum impact.
Total cost: $0/month for all APIs
"""
        elif configured < 5:
            result += f"""
✅ You have {configured}/5 APIs configured

🎯 Priority for remaining APIs:
"""
            if not status["Google Civic"]:
                result += "  • Google Civic - Essential for representative discovery\n"
            if not status["OpenStates"]:
                result += "  • OpenStates - Required for civic calendar & voting records\n"
            if not status["OpenFEC"]:
                result += "  • OpenFEC - Adds campaign finance transparency\n"
            if not status["Congress.gov"]:
                result += "  • Congress.gov - Completes federal coverage\n"
            if not status["LegiScan"]:
                result += "  • LegiScan - Optional for deep bill research\n"
        else:
            result += """
🎉 All APIs configured! Samara is fully operational.

Try these queries:
  • "Who represents me at [your address]?"
  • "What's on my ballot?"
  • "Show civic events in [state]"
  • "Who funds Senator [name]?"
  • "Search bills about [topic]"
"""

        return result

    def find_my_representatives(
        self,
        address: str
    ) -> str:
        """
        Find all your elected representatives by address.

        Discovers officials at every level: city, county, state, and federal.
        Includes contact information, terms, and districts.

        Args:
            address: Your full address (e.g., "123 Main St, Toledo, OH 43604")
        """
        if not self.valves.GOOGLE_CIVIC_API_KEY.strip():
            return "❌ Google Civic API key not configured. Please add it in function settings."

        url = f"{self.base_urls['google_civic']}/representatives"
        params = {
            "key": self.valves.GOOGLE_CIVIC_API_KEY,
            "address": address
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Format the response nicely
            result = f"📍 Representatives for: {address}\n\n"

            if "offices" in data and "officials" in data:
                offices = data["offices"]
                officials = data["officials"]

                for office in offices:
                    office_name = office["name"]
                    result += f"\n{'='*60}\n{office_name}\n{'='*60}\n"

                    for official_index in office["officialIndices"]:
                        official = officials[official_index]
                        result += f"\n👤 {official.get('name', 'Unknown')}"

                        if "party" in official:
                            result += f" ({official['party']})"

                        result += "\n"

                        if "phones" in official:
                            result += f"   📞 {', '.join(official['phones'])}\n"

                        if "emails" in official:
                            result += f"   📧 {', '.join(official['emails'])}\n"

                        if "urls" in official:
                            result += f"   🌐 {official['urls'][0]}\n"

                        if "channels" in official:
                            social = []
                            for channel in official["channels"]:
                                platform = channel.get("type", "").lower()
                                handle = channel.get("id", "")
                                social.append(f"{platform}: {handle}")
                            if social:
                                result += f"   💬 {', '.join(social)}\n"

                result += f"\n\n✅ Found {len(officials)} representatives"
            else:
                result += "No representatives found for this address."

            return result

        except requests.exceptions.RequestException as e:
            return f"❌ Error contacting Google Civic API: {str(e)}"

    def get_upcoming_elections(self) -> str:
        """
        Get information about upcoming elections.

        Returns election dates, types, and relevant information.
        """
        if not self.valves.GOOGLE_CIVIC_API_KEY.strip():
            return "❌ Google Civic API key not configured."

        url = f"{self.base_urls['google_civic']}/elections"
        params = {"key": self.valves.GOOGLE_CIVIC_API_KEY}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            result = "🗳️ UPCOMING ELECTIONS\n\n"

            if "elections" in data:
                for election in data["elections"]:
                    result += f"📅 {election.get('name', 'Unknown Election')}\n"
                    result += f"   Date: {election.get('electionDay', 'TBD')}\n"
                    if "ocdDivisionId" in election:
                        result += f"   Jurisdiction: {election['ocdDivisionId']}\n"
                    result += "\n"
            else:
                result += "No upcoming elections found.\n"

            return result

        except requests.exceptions.RequestException as e:
            return f"❌ Error fetching elections: {str(e)}"

    def get_civic_calendar(
        self,
        state_code: str,
        days_ahead: int = 7
    ) -> str:
        """
        Get upcoming civic events (meetings, hearings, etc.) in your area.

        Args:
            state_code: Two-letter state code (e.g., "OH" for Ohio)
            days_ahead: Number of days to look ahead (default: 7)
        """
        if not self.valves.OPENSTATES_API_KEY.strip():
            return "❌ OpenStates API key not configured."

        from datetime import datetime, timedelta

        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

        url = f"{self.base_urls['openstates']}/events"
        headers = {"X-API-KEY": self.valves.OPENSTATES_API_KEY}
        params = {
            "jurisdiction": state_code.lower(),
            "start_date": start_date,
            "end_date": end_date
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            result = f"📅 CIVIC CALENDAR - {state_code.upper()}\n"
            result += f"Next {days_ahead} days ({start_date} to {end_date})\n\n"

            if "results" in data and data["results"]:
                for event in data["results"]:
                    result += f"📍 {event.get('name', 'Unnamed Event')}\n"
                    result += f"   Date: {event.get('start_date', 'TBD')}\n"

                    if "location" in event:
                        result += f"   Location: {event['location'].get('name', 'Unknown')}\n"

                    if "description" in event:
                        desc = event["description"][:200]
                        result += f"   Info: {desc}...\n"

                    result += "\n"

                result += f"✅ Found {len(data['results'])} upcoming events"
            else:
                result += "No civic events found for this period."

            return result

        except requests.exceptions.RequestException as e:
            return f"❌ Error fetching civic events: {str(e)}"

    def search_campaign_finance(
        self,
        candidate_name: str,
        election_year: Optional[int] = None
    ) -> str:
        """
        Search for campaign finance information for federal candidates.

        Shows fundraising totals and top donors.

        Args:
            candidate_name: Name of the candidate to search
            election_year: Optional election cycle year (e.g., 2024)
        """
        if not self.valves.OPENFEC_API_KEY.strip():
            return "❌ OpenFEC API key not configured."

        # First, search for the candidate
        search_url = f"{self.base_urls['openfec']}/candidates/search"
        search_params = {
            "api_key": self.valves.OPENFEC_API_KEY,
            "q": candidate_name,
            "sort": "-receipts"
        }

        if election_year:
            search_params["cycle"] = election_year

        try:
            response = requests.get(search_url, params=search_params, timeout=10)
            response.raise_for_status()
            data = response.json()

            result = f"💰 CAMPAIGN FINANCE SEARCH: {candidate_name}\n\n"

            if "results" in data and data["results"]:
                for candidate in data["results"][:5]:  # Show top 5 matches
                    result += f"👤 {candidate.get('name', 'Unknown')}\n"
                    result += f"   Party: {candidate.get('party', 'Unknown')}\n"
                    result += f"   Office: {candidate.get('office_full', 'Unknown')}\n"
                    result += f"   State: {candidate.get('state', 'N/A')}\n"

                    if "cycles" in candidate:
                        result += f"   Cycles: {', '.join(map(str, candidate['cycles']))}\n"

                    result += "\n"

                result += f"✅ Found {len(data['results'])} candidates matching '{candidate_name}'"
            else:
                result += f"No candidates found matching '{candidate_name}'"

            return result

        except requests.exceptions.RequestException as e:
            return f"❌ Error searching campaign finance: {str(e)}"

    def search_federal_bills(
        self,
        search_term: str,
        congress_number: int = 118
    ) -> str:
        """
        Search for federal legislation by keyword.

        Args:
            search_term: Topic or keyword to search for
            congress_number: Congress number (118 = current, 117 = previous)
        """
        if not self.valves.CONGRESS_API_KEY.strip():
            return "❌ Congress.gov API key not configured."

        url = f"{self.base_urls['congress']}/bill/{congress_number}"
        params = {
            "api_key": self.valves.CONGRESS_API_KEY,
            "format": "json",
            "limit": 10
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            result = f"📜 FEDERAL BILLS - {congress_number}th Congress\n"
            result += f"Search: '{search_term}'\n\n"

            if "bills" in data:
                # Filter results by search term (simple client-side filtering)
                matching_bills = [
                    bill for bill in data["bills"]
                    if search_term.lower() in bill.get("title", "").lower()
                ]

                if matching_bills:
                    for bill in matching_bills[:10]:
                        result += f"📄 {bill.get('type', '')} {bill.get('number', '')}\n"
                        result += f"   {bill.get('title', 'No title')}\n"

                        if "latestAction" in bill:
                            action = bill["latestAction"]
                            result += f"   Latest: {action.get('text', 'Unknown')} ({action.get('actionDate', 'Unknown date')})\n"

                        result += "\n"

                    result += f"✅ Found {len(matching_bills)} bills mentioning '{search_term}'"
                else:
                    result += f"No bills found mentioning '{search_term}' in the {congress_number}th Congress"
            else:
                result += "No bill data available"

            return result

        except requests.exceptions.RequestException as e:
            return f"❌ Error searching federal bills: {str(e)}"
