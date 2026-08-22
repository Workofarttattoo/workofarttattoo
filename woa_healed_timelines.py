#!/usr/bin/env python3
"""Portfolio-linked healed timelines and client case studies (factual, no fabricated reviews)."""

from __future__ import annotations

from dataclasses import dataclass

SITE = "https://www.workofarttattoo.com"
PORTFOLIO = f"{SITE}/home_work_of_art_tattoo_piercing/client-portfolio"


@dataclass(frozen=True)
class TimelineStage:
    label: str
    note: str
    image_stem: str | None = None


@dataclass(frozen=True)
class CaseStudy:
    title: str
    artist: str
    placement: str
    sessions: str
    summary: str
    stages: tuple[TimelineStage, ...]
    guide_href: str | None = None
    image_stem: str | None = None
    image_dir: str = "home_work_of_art_tattoo_piercing/client-portfolio"


def image_url(stem: str, *, webp: bool = True) -> str:
    ext = "webp" if webp else "png"
    return f"{PORTFOLIO}/{stem}.{ext}"


JOSHUA_CASE_STUDIES: tuple[CaseStudy, ...] = (
    CaseStudy(
        title="Black & grey lion thigh",
        artist="Joshua Cole",
        placement="Outer thigh",
        sessions="Two sessions, ~12 hours total",
        summary=(
            "Collector wanted a large lion with open skin for highlights — not a solid black fill. "
            "We mapped contrast for desert sun and scheduled a second pass after the first layer settled."
        ),
        stages=(
            TimelineStage("Fresh (day 0)", "Wrapped with second skin; deep blacks set, highlights left open."),
            TimelineStage("4 weeks healed", "Peeling finished; mid-tones read cleanly in daylight."),
            TimelineStage("3+ months", "Blacks stayed saturated; no muddy grey wash in the thigh bend."),
        ),
        guide_href="/realism_tattoos_las_vegas_master_authority_guide/",
        image_stem="black-grey-lion-thigh-realism-las-vegas",
    ),
    CaseStudy(
        title="Skull & hourglass forearm",
        artist="Joshua Cole",
        placement="Forearm",
        sessions="Single long session",
        summary=(
            "Fine grey transitions around the hourglass glass — the kind of piece that fails if "
            "values are too soft on day one."
        ),
        stages=(
            TimelineStage("Fresh (day 0)", "Documented at bandage-off; glass highlights from negative space."),
            TimelineStage("4 weeks healed", "Linework and grey steps still separated — no blowout."),
            TimelineStage("3+ months", "Readable from arm's length; client returned for a touch-up consult only."),
        ),
        guide_href="/realism_tattoos_las_vegas_master_authority_guide/",
        image_stem="skull-hourglass-forearm-realism-fresh-las-vegas",
    ),
    CaseStudy(
        title="Cover-up: phoenix hand & forearm",
        artist="Joshua Cole",
        placement="Hand and forearm",
        sessions="Multiple sessions over several months",
        summary=(
            "Old color work needed a full redesign — not a darker blob. We planned warm tones and "
            "session spacing so the hand could heal between passes."
        ),
        stages=(
            TimelineStage("Before consult", "Faded color documented in-studio — no stock before/after collage."),
            TimelineStage("Mid-project", "Large areas rebuilt; client healed between hand and forearm passes."),
            TimelineStage("Finished & healed", "Phoenix reads as new art, not a patch over old ink."),
        ),
        guide_href="/cover_up_tattoos_las_vegas_master_authority_guide/",
        image_stem="cover-up-tattoo-phoenix-hand-las-vegas-after",
        image_dir="cover_up_tattoos_las_vegas_master_authority_guide",
    ),
)

KATELYN_CASE_STUDIES: tuple[CaseStudy, ...] = (
    CaseStudy(
        title="Ear curation — helix & flat constellation",
        artist="Katelyn Cole",
        placement="Left ear",
        sessions="Two appointments (planning + install)",
        summary=(
            "Client wanted a balanced constellation without crowding the helix. We measured anatomy, "
            "picked implant-grade titanium, and staged piercings so swelling on one side did not "
            "complicate the other."
        ),
        stages=(
            TimelineStage("Day 0", "Sterile setup, marked placement, titanium installed."),
            TimelineStage("6 weeks", "Swelling down; downsizing consult if needed."),
            TimelineStage("3+ months", "Stable angles; ready for curated jewelry upgrades."),
        ),
        guide_href="/best_piercing_shop_las_vegas_updated_jewelry_standards/",
        image_stem="ear-curation-work-eb7d2939",
        image_dir="studio_gallery",
    ),
)
