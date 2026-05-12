import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)


class GoogleAdsClient:
    """Wrapper around the Google Ads API Keyword Planner.

    Uses the google-ads Python library. Falls back gracefully when
    credentials are missing so the app works without Google Ads setup.
    """

    def __init__(self):
        self._client = None
        self._customer_id: Optional[str] = None
        self._ready = False
        self._init()

    def _init(self):
        if not settings.google_ads_developer_token:
            logger.info("Google Ads: GOOGLE_ADS_DEVELOPER_TOKEN not set — skipping")
            return
        if not settings.google_ads_client_id:
            logger.info("Google Ads: GOOGLE_ADS_CLIENT_ID not set — skipping")
            return

        try:
            from google.ads.googleads.client import GoogleAdsClient as _GoogleAdsClient

            credentials = {
                "developer_token": settings.google_ads_developer_token,
                "client_id": settings.google_ads_client_id,
                "client_secret": settings.google_ads_client_secret or "",
                "refresh_token": settings.google_ads_refresh_token or "",
                "use_proto_plus": False,
            }

            if settings.google_ads_login_customer_id:
                credentials["login_customer_id"] = settings.google_ads_login_customer_id

            self._client = _GoogleAdsClient.load_from_dict(credentials)
            self._customer_id = settings.google_ads_customer_id
            self._ready = True
            logger.info("Google Ads client initialised")
        except Exception as exc:
            logger.warning("Google Ads init failed — will use fallback scoring: %s", exc)

    def _get_service(self):
        if not self._ready:
            return None
        return self._client.get_service("KeywordPlanIdeaService")

    def get_keyword_ideas(self, keywords: list[str], language: str = "en", location: str = "KE") -> dict[str, dict]:
        """Fetch search volume and competition data for a list of keywords.

        Returns a dict keyed by keyword:
            {"keyword": {"avg_monthly_searches": int, "competition": str, "low_bid": float, "high_bid": float}}
        Returns empty dict if Google Ads is not configured or on error.
        """
        service = self._get_service()
        if not service:
            return {}

        try:
            request = self._client.get_type("GenerateKeywordIdeasRequest")
            request.customer_id = self._customer_id
            request.language = language
            request.geo_target_constants.append(f"geoTargetConstants/{self._geo_code(location)}")
            request.include_legacy_response = False

            request.keyword_plan_network = self._client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
            for kw in keywords[:50]:
                request.keyword_seed.keywords.append(kw)

            response = service.generate_keyword_ideas(request=request)
            return self._parse_response(response)

        except Exception as exc:
            logger.warning("Google Ads Keyword Planner error: %s", exc)
            return {}

    def _geo_code(self, country: str) -> str:
        codes = {"KE": "22107", "US": "2840", "GB": "2826"}
        return codes.get(country, "22107")

    def _parse_response(self, response) -> dict[str, dict]:
        result = {}
        for idea in response:
            kw = idea.text
            metrics = idea.keyword_idea_metrics
            result[kw] = {
                "avg_monthly_searches": metrics.avg_monthly_searches if metrics else 0,
                "competition": metrics.competition.name if metrics else "UNKNOWN",
                "low_bid": metrics.low_top_of_page_bid_micros / 1e6 if metrics else 0,
                "high_bid": metrics.high_top_of_page_bid_micros / 1e6 if metrics else 0,
            }
        return result


google_ads = GoogleAdsClient()
