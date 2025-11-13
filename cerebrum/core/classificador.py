"""Classificador: Decides taxonomy and framework placement.

Determines:
- Domain and subdomain
- BASB: PARA path (Projects/Areas/Resources/Archives)
- LYT: Relevant MOCs
- Tags (hierarchical)
- Content type classification

Simple but effective: LLM-based with structured output.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import json
import re

from cerebrum.services.llm_service import LLMService


class ClassificadorAgent:
    """Classifies content for proper taxonomy placement."""

    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

        # Default taxonomy
        self.known_domains = [
            'neuroscience', 'philosophy', 'systems', 'computer-science',
            'mathematics', 'psychology', 'biology', 'physics', 'chemistry',
            'economics', 'sociology', 'literature', 'history', 'art',
            'business', 'education', 'health', 'engineering'
        ]

    def classify(
        self,
        raw_text: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Classify content for taxonomy placement.

        Args:
            raw_text: Extracted text
            metadata: Extraction metadata

        Returns:
            Classification dict with:
                - domain, subdomain
                - basb_para_category, basb_para_path
                - lyt_mocs (list of MOC names)
                - tags (hierarchical list)
                - content_type
        """

        # Determine source type
        source_type = metadata.get('source_type', 'unknown')
        title = metadata.get('title', 'Untitled')

        # Build classification prompt
        prompt = self._build_classification_prompt(
            raw_text, title, source_type
        )

        # Get LLM classification
        response = self.llm.generate(prompt, max_tokens=500)

        # Parse response
        classification = self._parse_classification(response)

        # Build final classification
        result = {
            'domain': classification.get('domain', 'general'),
            'subdomain': classification.get('subdomain'),
            'basb_para_category': self._determine_para_category(source_type, classification),
            'basb_para_path': None,  # Will be set below
            'lyt_mocs': classification.get('mocs', []),
            'tags': self._build_hierarchical_tags(classification),
            'content_type': classification.get('content_type', 'concept'),
            'confidence': classification.get('confidence', 0.75)
        }

        # Build BASB path
        result['basb_para_path'] = self._build_para_path(result)

        return result

    def _build_classification_prompt(
        self,
        raw_text: str,
        title: str,
        source_type: str
    ) -> str:
        """Build classification prompt."""

        text_sample = raw_text[:2000]  # First 2000 chars

        return f"""You are an expert knowledge taxonomist.

Classify this content into a clear taxonomy.

**Title:** {title}
**Source Type:** {source_type}

**Content Sample:**
{text_sample}

Provide classification as JSON:
{{
  "domain": "primary domain (one of: {', '.join(self.known_domains[:10])}... or other)",
  "subdomain": "specific subdomain",
  "content_type": "concept|principle|model|evidence|mechanism|application",
  "mocs": ["MOC Name 1", "MOC Name 2"],
  "key_topics": ["topic1", "topic2", "topic3"],
  "confidence": 0.85
}}

Rules:
1. Domain: Choose most specific domain
2. Subdomain: Narrow specialty within domain
3. MOCs: 2-4 Maps of Content that should index this
4. Key topics: 3-6 specific topics covered

Return ONLY valid JSON, no other text.
"""

    def _parse_classification(self, response: str) -> Dict[str, Any]:
        """Parse LLM classification response."""

        try:
            # Extract JSON
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                classification = json.loads(json_match.group())
            else:
                classification = json.loads(response)

            return classification

        except json.JSONDecodeError:
            # Fallback: minimal classification
            return {
                'domain': 'general',
                'subdomain': None,
                'content_type': 'concept',
                'mocs': [],
                'key_topics': [],
                'confidence': 0.5
            }

    def _determine_para_category(
        self,
        source_type: str,
        classification: Dict[str, Any]
    ) -> str:
        """Determine BASB PARA category."""

        # Default: everything goes to Resources
        # (Projects and Areas require user context)

        if source_type in ['academic_paper', 'book', 'article']:
            return 'Resources'

        # Could be more sophisticated with user context
        return 'Resources'

    def _build_hierarchical_tags(
        self,
        classification: Dict[str, Any]
    ) -> list:
        """Build hierarchical tag list."""

        tags = []

        # Domain tags
        domain = classification.get('domain', 'general')
        subdomain = classification.get('subdomain')

        if domain:
            tags.append(f"{domain}")
            if subdomain:
                tags.append(f"{domain}/{subdomain}")

        # Content type tag
        content_type = classification.get('content_type', 'concept')
        tags.append(f"type/{content_type}")

        # Topic tags
        key_topics = classification.get('key_topics', [])
        for topic in key_topics[:5]:  # Max 5 topic tags
            tags.append(f"topic/{topic.lower().replace(' ', '-')}")

        # Framework tags
        tags.append('zk/permanent')  # Zettelkasten permanent note
        tags.append('basb/resource')  # BASB Resources

        return tags

    def _build_para_path(self, classification: Dict[str, Any]) -> str:
        """Build BASB PARA file path."""

        category = classification['basb_para_category']
        domain = classification['domain']

        # Map category to number prefix
        category_prefix = {
            'Projects': '1-Projects',
            'Areas': '2-Areas',
            'Resources': '3-Resources',
            'Archives': '4-Archives'
        }

        prefix = category_prefix.get(category, '3-Resources')

        # Map domain to number
        domain_map = {
            'neuroscience': '41-Neuroscience',
            'philosophy': '42-Philosophy',
            'systems': '43-Systems',
            'computer-science': '44-Computer-Science',
            'mathematics': '45-Mathematics',
            'psychology': '46-Psychology',
            'biology': '47-Biology',
            'physics': '48-Physics',
            'chemistry': '49-Chemistry'
        }

        domain_dir = domain_map.get(domain, f'40-{domain.title()}')

        return f"{prefix}/{domain_dir}"

    def validate_classification(
        self,
        classification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate classification result."""

        checks = {}

        # Check 1: Domain is specified
        checks['domain_present'] = {
            'passed': classification.get('domain') is not None,
            'message': 'Domain should be specified',
            'value': classification.get('domain')
        }

        # Check 2: PARA path exists
        checks['para_path_valid'] = {
            'passed': classification.get('basb_para_path') is not None,
            'message': 'BASB PARA path should be generated',
            'value': classification.get('basb_para_path')
        }

        # Check 3: At least one MOC suggested
        mocs = classification.get('lyt_mocs', [])
        checks['mocs_suggested'] = {
            'passed': len(mocs) >= 1,
            'message': 'Should suggest at least 1 MOC',
            'value': len(mocs)
        }

        # Check 4: Tags are hierarchical
        tags = classification.get('tags', [])
        checks['tags_present'] = {
            'passed': len(tags) >= 3,
            'message': 'Should have at least 3 tags',
            'value': len(tags)
        }

        all_passed = all(c['passed'] for c in checks.values())

        return {
            'passed': all_passed,
            'checks': checks,
            'summary': f"{'✅ PASSED' if all_passed else '❌ FAILED'}: {sum(c['passed'] for c in checks.values())}/{len(checks)} checks"
        }
