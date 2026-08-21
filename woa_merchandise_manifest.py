#!/usr/bin/env python3
"""Merchandise catalog — original art by Joshua Cole (migrated from legacy WP page)."""

from __future__ import annotations

from dataclasses import dataclass

SLUG = "merchandise"
CANON = f"https://workofarttattoo.com/{SLUG}/"


@dataclass(frozen=True)
class MerchItem:
    stem: str
    source_url: str
    title: str
    detail: str
    ext: str  # jpg | png | webp


MERCH_ITEMS: tuple[MerchItem, ...] = (
    MerchItem(
        "mixed-media-bristol-paper",
        "https://workofarttattoo.com/wp-content/uploads/2023/03/Mixed-media-on-Bristol-paper.png",
        "Mixed media on Bristol paper",
        "Original mixed-media piece on Bristol paper by Joshua Cole.",
        "png",
    ),
    MerchItem(
        "watercolor-canvas-board-1",
        "https://workofarttattoo.com/wp-content/uploads/2023/03/100-percent-cotton-pre-shrunk-t-shirts-available-in-Med-Large-XL-XXL-and-XXXL.png",
        "Watercolor on canvas board",
        "Original watercolor on canvas board — one of a kind.",
        "png",
    ),
    MerchItem(
        "watercolor-canvas-board-2",
        "https://workofarttattoo.com/wp-content/uploads/2023/03/100-percent-cotton-pre-shrunk-t-shirts-available-in-Med-Large-XL-XXL-and-XXXL-1.png",
        "Watercolor on canvas board",
        "Original watercolor on canvas board — one of a kind.",
        "png",
    ),
    MerchItem(
        "prismacolor-bristol-a7f622a6",
        "https://workofarttattoo.com/wp-content/uploads/2023/03/A7F622A6-F598-4D60-9EA0-180451BA7EFC-scaled.webp",
        "Prismacolor on Bristol paper",
        "Original Prismacolor illustration on Bristol paper by Joshua Cole.",
        "webp",
    ),
    MerchItem(
        "prismacolor-bristol-211002a1",
        "https://workofarttattoo.com/wp-content/uploads/2023/03/211002A1-E662-4490-BD9D-D6D8BB045790-scaled.webp",
        "Prismacolor on Bristol paper",
        "Original Prismacolor illustration on Bristol paper by Joshua Cole.",
        "webp",
    ),
    MerchItem(
        "prismacolor-bristol-6e3d8efa",
        "https://workofarttattoo.com/wp-content/uploads/2023/03/6E3D8EFA-58A6-4738-82F5-44BE99CBF0EC-scaled.webp",
        "Prismacolor on Bristol paper",
        "Another original Prismacolor piece by Joshua Cole at Work of Art Tattoo.",
        "webp",
    ),
    MerchItem(
        "graphite-archival-5x7-framed",
        "https://workofarttattoo.com/wp-content/uploads/2021/07/Hand-drawn-original-one-of-a-kind-piece-by-owner-Joshua-Cole.-Done-in-graphite-on-archival-paper.-Includes-frame.jpg",
        "Graphite on archival paper — framed",
        "Hand-drawn original one-of-a-kind piece by Joshua Cole. Graphite on archival paper, includes frame. Piece measures 5×7 inches.",
        "jpg",
    ),
    MerchItem(
        "graphite-8x11-inquire",
        "https://workofarttattoo.com/wp-content/uploads/2021/07/An-original-graphite-drawing-by-Joshua-Cole.-8.5-x-11-inches.-Inquire-for-price.jpg",
        "Graphite drawing — 8.5 × 11 in.",
        "An original graphite drawing by Joshua Cole. 8.5 × 11 inches. Inquire for price.",
        "jpg",
    ),
    MerchItem(
        "prismacolor-bristol-be3f887f",
        "https://workofarttattoo.com/wp-content/uploads/2023/03/BE3F887F-F974-413A-AB72-AC64DA7F9360-scaled.webp",
        "Prismacolor on Bristol paper",
        "Original Prismacolor illustration on Bristol paper by Joshua Cole.",
        "webp",
    ),
    MerchItem(
        "graphite-drive-by-framed",
        "https://workofarttattoo.com/wp-content/uploads/2021/07/Another-original-drawing-by-Joshua-Cole-done-in-graphite.-8.5X11-inches.-Includes-frame.-Titled-Drive-by.jpg",
        '"Drive by" — graphite, framed',
        '"Drive by" — another original drawing by Joshua Cole in graphite. 8.5 × 11 inches, includes frame.',
        "jpg",
    ),
    MerchItem(
        "graphite-colored-pencil-hand-framed",
        "https://workofarttattoo.com/wp-content/uploads/2021/07/hand.jpg",
        "Graphite & colored pencil — framed",
        "One-of-a-kind original hand-drawn piece under glass by Joshua Cole. Graphite and colored pencil, includes frame. Art is 8.5 × 11 inches; outer frame is larger.",
        "jpg",
    ),
    MerchItem(
        "colored-pencil-bridges-framed",
        "https://workofarttattoo.com/wp-content/uploads/2021/07/20210707_114132.jpg",
        '"May the bridges I\'ve burned, light my way."',
        "One-of-a-kind original in colored pencil on archival paper by Joshua Cole. Titled \"May the bridges I've burned, light my way.\" Includes frame.",
        "jpg",
    ),
)
