#!/usr/bin/env python3
"""Offsite booking media — private events and VIP house calls."""

from __future__ import annotations

from dataclasses import dataclass

from woa_studio_media_manifest import slugify


@dataclass(frozen=True)
class OffsiteEvent:
    slug: str
    heading: str
    blurb: str
    uuid_prefixes: tuple[str, ...]


@dataclass(frozen=True)
class OffsiteMediaItem:
    uuid_prefix: str
    stem: str
    event_slug: str
    title: str
    alt: str


# Standout photos — remainder get numbered session titles.
TYSON_KNOWN: dict[str, tuple[str, str]] = {
    "CE767869": (
        "VIP party overview",
        "Crowded luxury event with illuminated fountain — offsite tattoo booking at Mike Tyson's house, Joshua Cole Work of Art Las Vegas",
    ),
    "0D9B5525": (
        "Mobile studio banner setup",
        "Work of Art Tattoo mobile banner and sterile supply station — offsite booking Las Vegas",
    ),
    "68ECDECB": (
        "Bitcoin logo tattoo",
        "Small Bitcoin logo tattoo completed at private offsite event — Joshua Cole, Work of Art Las Vegas",
    ),
    "5E1AE4DA": (
        "Smiley flash stencils",
        "Smiley-face flash stencil sheet prepared for party guests — offsite event tattooing",
    ),
    "1A9B08FD": (
        "Design consult on iPad",
        "Joshua Cole reviewing tattoo designs with client at portable offsite station",
    ),
    "300EED85": (
        "Portable tattoo station prep",
        "Joshua Cole setting up pink portable table with professional lighting — offsite house call",
    ),
    "FEFA7046": (
        "Hand tattoo session",
        "Joshua Cole tattooing client's hand at private residence — offsite booking Work of Art Las Vegas",
    ),
    "2026B305": (
        "Ear tattoo session",
        "Joshua Cole tattooing at private event — portable setup with professional lighting",
    ),
    "892CCE83": (
        "Joshua at offsite setup",
        "Joshua Cole at portable tattoo station — Work of Art Las Vegas offsite booking",
    ),
    "283378EA": (
        "Offsite workspace",
        "Mobile tattoo workspace with Work of Art banner — private event Las Vegas",
    ),
    "9EFAB4AF": (
        "Stencil placement",
        "Joshua Cole applying tattoo stencil at offsite private event",
    ),
    "B619EDC6": (
        "Client session in progress",
        "Tattoo session at upscale private residence — Joshua Cole offsite booking",
    ),
    "8EDE3196": (
        "Delicate placement work",
        "Joshua Cole working on small tattoo at private party — Work of Art Las Vegas",
    ),
    "E857E59A": (
        "Live session documentation",
        "Offsite tattoo session filmed at VIP private event — Joshua Cole",
    ),
    "12AE711E": (
        "Pre-session consult",
        "Joshua Cole and client preparing for tattoo at portable offsite station",
    ),
    "6FFEBC20": (
        "Party tattoo session",
        "Joshua Cole tattooing at private residence event — Work of Art Las Vegas",
    ),
    "11A563EB": (
        "Offsite client work",
        "Completed tattoo work at private offsite booking — Joshua Cole Las Vegas",
    ),
    "443A4644": (
        "Event tattoo portfolio",
        "Black and grey tattoo work from private offsite event — Joshua Cole",
    ),
    "E016E3AA": (
        "Private event tattoo",
        "Custom tattoo completed at Mike Tyson house party — Joshua Cole Work of Art Las Vegas",
    ),
    "00BC3C55": ("Forearm work beside lion statue", "Joshua Cole tattoos forearm on pink table beside lion statue and boxing mural offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "05F97CD3": ("Forearm session under studio banner", "Joshua Cole tattoos forearm at pink table beneath Work of Art Las Vegas skull banner — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "082676BE": ("Forearm tattoo by boxing mural", "Joshua Cole tattoos client's forearm at pink table with boxing mural behind offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "0F9EE73E": ("Wiping fresh back tattoo clean", "Joshua Cole wipes fresh ornate back tattoo on smiling blonde client at offsite event — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "110DD123": ("Joshua Cole smiles before ear tattoo", "Joshua Cole smiles, machine ready behind client's ear stencil — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "12A987BD": ("Fresh Bitcoin logo shoulder tattoo", "Fresh Bitcoin logo tattoo on shoulder beside faded black-grey back piece offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "12D3DEA2": ("Finished power button neck tattoo", "Fresh black power-button neck tattoo behind red-haired client's ear, finished offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "25EDDBB8": ("Joyful client mid-party tattoo session", "Client grins wide on pink tattoo table with festival wristbands at VIP party — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "28A927F5": ("Finished back tattoo reveal offsite", "Blonde client turns showing finished ornate back tattoo at pink offsite event table — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "33FACF49": ("Smiley finger covers client's mouth", "Smiley finger tattoo covers man's mouth; spear forearm and heart hand at offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "38689C86": ("Artist prepares offsite supplies", "Joshua Cole opens tattoo supplies at pink table facing client in KIVA jersey, lion statue — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "40FF2F83": ("Power button neck tattoo session", "Joshua Cole tattoos power-button icon on neck behind client's ear at offsite event — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "4466A651": ("Overhead view of neck tattoo work", "Overhead of Joshua Cole tattooing behind client's ear with rotary gun — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "46BE4419": ("Ear cartilage tattoo offsite", "Joshua Cole tattoos woman's ear cartilage on pink table in chandelier-lit hotel suite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "4BF878AD": ("Client poses on tattoo chair", "Smiling blonde client poses on white tattoo armrest showing fresh shoulder ink offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "4F30C0BB": ("Joshua Cole smiles during neck tattoo", "Joshua Cole tattoos jawline stencil on red-haired client in #21 jersey — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "533F90BC": ("Joshua inks ornate back piece", "Joshua Cole inks ornate black-grey back tattoo on blonde client leaning forward — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "562D7E48": ("Joshua Cole holds wrap and tattoo machine", "Joshua Cole smiles holding barrier film and wrapped machine at WOA banner — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "59D997F0": ("Joshua Cole opens ink before neck tattoo", "Joshua Cole opens ink bottle as client waits with purple neck stencil — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "5CE7739D": ("Script tattoo behind ear offsite", "Joshua Cole tattoos purple script behind client's ear on pink-wrapped offsite station — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "67E16651": ("Hand tattoo at pink station", "Joshua Cole tattoos back of hand on pink table; client has arrow forearm tattoo — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "712AC10D": ("Close-up temple and ear tattoo session", "Close-up of Joshua Cole tattooing client's temple and ear area — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "7692F658": ("Lion statue at event venue", "Lion statue overlooks boxing mural and chandelier in Vegas hotel mezzanine lounge — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "780DC356": ("Arrow tattoo at pink table", "Men sit at pink offsite table; client shows fresh arrow forearm tattoo near lion statue — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "79958590": ("Artist wipes phoenix back tattoo", "Joshua Cole wipes fresh phoenix back tattoo as laughing blonde client reacts offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "7B9C7784": ("Client films arm tattoo on pink table", "Client on pink table films Joshua Cole tattooing her arm with phone selfie — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "8074A709": ("Back piece over faded portrait", "Joshua Cole tattoos upper back beside faded blue portrait on blonde client offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "8E384AC0": ("Small hand tattoo beside arrow", "Joshua Cole tattoos small design on hand beside arrow-and-rose forearm at pink table — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "91135235": ("Neck tattoo on pink portable table", "Joshua Cole tattoos neck on client lying on pink plastic-wrapped table — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "9C77A1EA": ("Excited client on pink tattoo table", "Red-haired client laughs on pink-wrap table wearing orange Stacks wristbands — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "9DA92236": ("Hand tattoo on pink table", "Joshua Cole tattoos back of client's hand on pink-wrapped table; arrow on forearm — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "9FCF823D": ("Joshua Cole poses with barrier film roll", "Joshua Cole grins holding clear barrier film roll at mobile banner — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "A68626AC": ("Upper back tattoo on client", "Joshua Cole tattoos upper back on blonde client leaning on portable chair at offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "A8CBBA51": ("Neck placement consult on pink table", "Joshua Cole marks neck spot behind client's ear at pink portable table — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "AA92F551": ("Arrow inner forearm tattoo session", "Joshua Cole tattoos black arrow on inner forearm at pink table with Vegas banner behind — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "AAF52D4F": ("Consultation at pink offsite table", "Joshua Cole consults blonde client across pink massage table with LED lights at offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "B2BED9B8": ("Client mirror selfie showing tattoos", "Heavily tattooed client mirror selfie showing rose hand tattoo and purple butterfly offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "B37B1E86": ("Forearm tattoo with onlookers", "Joshua Cole tattoos client's inner forearm as onlookers watch at pink offsite station — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "BC20F686": ("Crowd gathers at Vegas venue", "Crowd gathers on balcony above lion statue beneath crystal chandelier at Vegas venue — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "C0F701C1": ("Upper back tattoo in progress", "Joshua Cole tattoos upper-back piece on blonde client in Raiders jersey setup — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "C1E8A694": ("Finished arrow forearm tattoo shown", "Client displays finished black arrow forearm tattoo at pink-covered offsite event table — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "C49CFFBF": ("Smiley hand tattoo gag photo", "Smiley hand tattoo covers man's mouth beside spear forearm tattoo at pink offsite table — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "C61315DF": ("Artist steadies back tattoo skin", "Gloved artist steadies skin on lower back beside ornate female face tattoo at offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "CE39DEE6": ("Digital tattoo design consult on tablet", "Blonde client watches Joshua Cole draw tattoo design on tablet — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "DB0E4C0A": ("Spider stomach tattoo mirror selfie", "Client mirror selfie showing black widow spider stomach tattoo and full body ink offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "DD5CFA25": ("Hand tattoo on client with mullet", "Joshua Cole tattoos client's hand on pink table; mullet client faces camera — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "EBEB19D1": ("Joshua wipes fresh back tattoo", "Joshua Cole wipes fresh anchor back tattoo on smiling blonde client indoors — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "EBFFBF9A": ("Fresh back piece reveal at event", "Blonde client smiles showing new shoulder-back tattoo beside Joshua Cole — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "EC284EB3": ("Hand tattoo near lion statue", "Arrow forearm tattoo on pink table beside lion statue and boxing mural at offsite — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "F2783418": ("Forearm tattoo while client holds beer", "Joshua Cole tattoos forearm as mullet client holds Modelo on pink table — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "F3971885": ("Cleaning fresh back tattoo offsite", "Joshua Cole wipes fresh back tattoo on smiling blonde woman at crowded offsite setup — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "F5DF31B6": ("Hand tattoo under Vegas banner", "Joshua Cole tattoos client's hand on pink table beneath Work of Art Las Vegas banner — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "F7412EF2": ("Artist tattoos rose under banner", "Joshua Cole tattoos black-grey rose on forearm beneath Work of Art Las Vegas banner — Joshua Cole offsite booking, Work of Art Las Vegas"),

    "FBDA035F": ("Rose forearm tattoo at offsite", "Raiders jersey artist tattoos rose on forearm at pink-covered offsite table — Joshua Cole offsite booking, Work of Art Las Vegas"),

}

TYSON_PARTY_PREFIXES: tuple[str, ...] = (
    "533F90BC",
    "BC20F686",
    "FBDA035F",
    "F7412EF2",
    "40FF2F83",
    "7692F658",
    "EC284EB3",
    "46BE4419",
    "B37B1E86",
    "780DC356",
    "9DA92236",
    "C0F701C1",
    "12D3DEA2",
    "8074A709",
    "00BC3C55",
    "C49CFFBF",
    "05F97CD3",
    "082676BE",
    "C1E8A694",
    "38689C86",
    "F5DF31B6",
    "0F9EE73E",
    "8E384AC0",
    "4BF878AD",
    "AA92F551",
    "12A987BD",
    "A68626AC",
    "F3971885",
    "C61315DF",
    "67E16651",
    "B2BED9B8",
    "28A927F5",
    "33FACF49",
    "DB0E4C0A",
    "79958590",
    "5CE7739D",
    "AAF52D4F",
    "4F30C0BB",
    "562D7E48",
    "91135235",
    "59D997F0",
    "712AC10D",
    "4466A651",
    "CE39DEE6",
    "9FCF823D",
    "DD5CFA25",
    "F2783418",
    "110DD123",
    "7B9C7784",
    "9C77A1EA",
    "25EDDBB8",
    "EBEB19D1",
    "EBFFBF9A",
    "2026B305",
    "FEFA7046",
    "0D9B5525",
    "68ECDECB",
    "300EED85",
    "1A9B08FD",
    "CE767869",
    "892CCE83",
    "283378EA",
    "9EFAB4AF",
    "B619EDC6",
    "8EDE3196",
    "5E1AE4DA",
    "E857E59A",
    "12AE711E",
    "A8CBBA51",
    "6FFEBC20",
    "11A563EB",
    "443A4644",
    "E016E3AA",
)

OFFSITE_EVENTS: tuple[OffsiteEvent, ...] = (
    OffsiteEvent(
        slug="party-at-mike-tysons-house",
        heading="Party at Mike Tyson's House",
        blurb=(
            "Joshua Cole brought a full mobile studio to a private VIP event — sterile setup, "
            "professional lighting, flash sheets, and custom work on guests throughout the night."
        ),
        uuid_prefixes=TYSON_PARTY_PREFIXES,
    ),
)


def classify_offsite(uuid_prefix: str, event_slug: str, index: int) -> OffsiteMediaItem:
    if uuid_prefix in TYSON_KNOWN:
        title, alt = TYSON_KNOWN[uuid_prefix]
    else:
        raise ValueError(
            f"Missing offsite alt catalog entry for {uuid_prefix} — run apply_media_alt_catalog.py"
        )
    stem = f"{slugify(title)}-{uuid_prefix[:8].lower()}"
    return OffsiteMediaItem(
        uuid_prefix=uuid_prefix,
        stem=stem,
        event_slug=event_slug,
        title=title,
        alt=alt,
    )


def offsite_manifest_items() -> list[OffsiteMediaItem]:
    out: list[OffsiteMediaItem] = []
    for event in OFFSITE_EVENTS:
        for i, prefix in enumerate(event.uuid_prefixes, 1):
            out.append(classify_offsite(prefix, event.slug, i))
    return out
