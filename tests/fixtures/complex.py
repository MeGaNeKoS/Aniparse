from aniparse.output_schemas import VideoResolution, SequenceNumber, SequenceIdentifierNumber, SequenceRange, SeriesInfo, Metadata

complex_cases = [
    Metadata(
        file_name="fairy tail - s06e32 - tartaros arc iron fist of the fire dragon [episode 83]",
        series=[
            SeriesInfo(
                title="fairy tail",
                season=[
                    SequenceNumber(
                        number=6
                    )
                ],
                episode=[
                    SequenceNumber(
                        number=32,
                        alternative=[
                            SequenceNumber(
                                number=83
                            )
                        ],
                        title="tartaros arc iron fist of the fire dragon"
                    )
                ]
            )
        ]
    ),
    Metadata(
        audio_term=[
            "dual audio"
        ],
        file_name="[animerg] shingeki no kyojin (the final season) - 13 [1080p 10bit dual audio] (attack on titan - 72)",
        release_group=[
            "animerg"
        ],
        series=[
            SeriesInfo(
                title="shingeki no kyojin (the final season)",
                episode=[
                    SequenceNumber(
                        number=13
                    )
                ]
            ),
            SeriesInfo(
                title="attack on titan",
                episode=[
                    SequenceNumber(
                        number=72
                    )
                ]
            )
        ],
        video_resolution=[
            VideoResolution(
                video_height=1080,
                scan_method="p"
            )
        ],
        video_term=[
            "10bit"
        ]
    ),
    Metadata(
        file_checksum="5203142b",
        file_name="[deep] tegami bachi (reverse) - letter bee - 29 (04) [5203142b]",
        release_group=[
            "deep"
        ],
        series=[
            SeriesInfo(
                title="tegami bachi (reverse) - letter bee",
                episode=[
                    SequenceNumber(
                        number=29,
                        alternative=[
                            SequenceNumber(
                                number=4
                            )
                        ]
                    )
                ]
            )
        ]
    ),
    Metadata(
        file_checksum="9df6b8d5",
        file_name="[hatsuyuki-kaitou]_fairy_tail_2_-_52_(227)_[720p][10bit][9df6b8d5]",
        release_group=[
            "hatsuyuki-kaitou"
        ],
        series=[
            SeriesInfo(
                title="fairy tail 2",
                episode=[
                    SequenceNumber(
                        number=52,
                        alternative=[
                            SequenceNumber(
                                number=227
                            )
                        ]
                    )
                ]
            )
        ],
        video_resolution=[
            VideoResolution(
                video_height=720,
                scan_method="p"
            )
        ],
        video_term=[
            "10bit"
        ]
    ),
    Metadata(
        file_checksum="dd66afb7",
        file_name="[hatsuyuki] dragon ball kai (2014) - 002 (100) [1280x720][dd66afb7]",
        release_group=[
            "hatsuyuki"
        ],
        series=[
            SeriesInfo(
                title="dragon ball kai",
                year=[
                    SequenceNumber(
                        number=2014
                    )
                ],
                episode=[
                    SequenceNumber(
                        number=2,
                        alternative=[
                            SequenceNumber(
                                number=100
                            )
                        ]
                    )
                ]
            )
        ],
        video_resolution=[
            VideoResolution(
                video_height=720,
                video_width=1280
            )
        ]
    ),
    Metadata(
        file_checksum="619c57a0",
        file_name="[hatsuyuki]_kuroko_no_basuke_s3_-_01_(51)_[720p][10bit][619c57a0]",
        release_group=[
            "hatsuyuki"
        ],
        series=[
            SeriesInfo(
                title="kuroko no basuke",
                season=[
                    SequenceNumber(
                        number=3
                    )
                ],
                episode=[
                    SequenceNumber(
                        number=1,
                        alternative=[
                            SequenceNumber(
                                number=51
                            )
                        ]
                    )
                ]
            )
        ],
        video_resolution=[
            VideoResolution(
                video_height=720,
                scan_method="p"
            )
        ],
        video_term=[
            "10bit"
        ]
    ),
    Metadata(
        file_name="[judas] gintama - s02e01-e02 (025-026)",
        release_group=[
            "judas"
        ],
        series=[
            SeriesInfo(
                title="gintama",
                season=[
                    SequenceNumber(
                        number=2
                    )
                ],
                episode=[
                    SequenceRange(
                        start=SequenceNumber(
                            number=1
                        ),
                        end=SequenceNumber(
                            number=2
                        ),
                        alternative=[
                            SequenceRange(
                                start=SequenceNumber(
                                    number=25
                                ),
                                end=SequenceNumber(
                                    number=26
                                )
                            )
                        ]
                    )
                ]
            )
        ]
    ),
    Metadata(
        audio_term=[
            "Dual Audio",
            "AAC"
        ],
        file_name="[Anime Time] Sword Art Online (S01+S02+S03+S04+Alternative+Movies+Specials+OVAs) [BD] [Dual Audio][1080p][HEVC 10bit x265][AAC][Eng Sub] [Batch] (SAO)",
        language=[
            "Eng"
        ],
        release_group=[
            "Anime Time"
        ],
        series=[
            SeriesInfo(
                title="Sword Art Online",
                season=[
                    SequenceNumber(
                        number=1
                    )
                ]
            ),
            SeriesInfo(
                title="Sword Art Online",
                season=[
                    SequenceNumber(
                        number=2
                    )
                ]
            ),
            SeriesInfo(
                title="Sword Art Online",
                season=[
                    SequenceNumber(
                        number=3
                    )
                ]
            ),
            SeriesInfo(
                title="Sword Art Online",
                season=[
                    SequenceNumber(
                        number=4
                    )
                ]
            ),
            SeriesInfo(
                title="Sword Art Online Alternative"
            ),
            SeriesInfo(
                title="Sword Art Online",
                type="Movies"
            ),
            SeriesInfo(
                title="Sword Art Online",
                type="Specials"
            ),
            SeriesInfo(
                title="Sword Art Online",
                type="OVAs"
            )
        ],
        source=[
            "BD"
        ],
        subs_term=[
            "Sub"
        ],
        video_resolution=[
            VideoResolution(
                video_height=1080,
                scan_method="p"
            )
        ],
        video_term=[
            "HEVC",
            "10bit",
            "x265"
        ]
    ),
    Metadata(
        file_name="SNK Anime (1993-2018) - Art of Fighting, Fatal Fury, Samurai Shodown, The King of Fighters - 480p-720p x264",
        unknown=[
            "Art of Fighting",
            "Fatal Fury",
            "Samurai Shodown",
            "The King of Fighters"
        ],
        series=[
            SeriesInfo(
                title="SNK Anime",
                year=[
                    SequenceRange(
                        start=SequenceNumber(
                            number=1993
                        ),
                        end=SequenceNumber(
                            number=2018
                        )
                    )
                ]
            )
        ],
        video_resolution=[
            VideoResolution(
                video_height=480,
                scan_method="p"
            ),
            VideoResolution(
                video_height=720,
                scan_method="p"
            )
        ],
        video_term=[
            "x264"
        ]
    ),
    Metadata(
        file_name="[Judas] Kaguya-Sama Wa Kokurasetai - S03E13v2 (S03E12 Part 2).mkv",
        release_group=[
            "Judas"
        ],
        series=[
            SeriesInfo(
                title="Kaguya-Sama Wa Kokurasetai",
                season=[
                    SequenceNumber(
                        number=3
                    )
                ],
                episode=[
                    SequenceNumber(
                        alternative=[
                            SequenceNumber(
                                number=12,
                                part="2"
                            )
                        ],
                        number=13,
                        release_version="2"
                    )
                ]
            )
        ]
    ),
    # --- Torrent name samples with | alternatives ---
    Metadata(
        audio_term=[
            "AAC"
        ],
        file_checksum="CC841FA8",
        file_name="[Yameii] TRIGUN STAMPEDE - S02E04 [English Dub] [CR WEB-DL 1080p H264 AAC] [CC841FA8] (TRIGUN STARGAZE | Season 2 | S2)",
        language=[
            "English"
        ],
        release_group=[
            "Yameii"
        ],
        series=[
            SeriesInfo(
                title="TRIGUN STAMPEDE",
                season=[
                    SequenceNumber(
                        number=2
                    )
                ],
                episode=[
                    SequenceNumber(
                        number=4
                    )
                ]
            ),
            SeriesInfo(
                title="TRIGUN STARGAZE"
            )
        ],
        source=[
            "WEB-DL"
        ],
        subs_term=[
            "Dub"
        ],
        video_resolution=[
            VideoResolution(
                video_height=1080,
                scan_method="p"
            )
        ],
        video_term=[
            "H264"
        ]
    ),
    Metadata(
        audio_term=[
            "DTS-HD MA",
            "Dual Audio"
        ],
        file_name="[ZQ] Street Fighter II: The Animated Movie (1994) (BD Remux 1080p x264 8-bit DTS-HD MA) [Dual Audio] | Street Fighter II: The Movie",
        release_group=[
            "ZQ"
        ],
        series=[
            SeriesInfo(
                title="Street Fighter II: The Animated Movie",
                year=[
                    SequenceNumber(
                        number=1994
                    )
                ]
            ),
            SeriesInfo(
                title="Street Fighter II: The Movie"
            )
        ],
        release_information=[
            "Remux"
        ],
        source=[
            "BD"
        ],
        video_resolution=[
            VideoResolution(
                video_height=1080,
                scan_method="p"
            )
        ],
        video_term=[
            "x264",
            "8-bit"
        ]
    ),
    Metadata(
        audio_term=[
            "FLAC",
            "Dual Audio"
        ],
        file_name="[UnHoly] Kaiju No. 8 Season 2 (BD Remux 1080p x264 8-bit FLAC) [Dual Audio] | Kaijuu 8-gou 2nd Season",
        release_group=[
            "UnHoly"
        ],
        series=[
            SeriesInfo(
                title="Kaiju No. 8",
                season=[
                    SequenceNumber(
                        number=2
                    )
                ]
            ),
            SeriesInfo(
                title="Kaijuu 8-gou 2nd Season"
            )
        ],
        release_information=[
            "Remux"
        ],
        source=[
            "BD"
        ],
        video_resolution=[
            VideoResolution(
                video_height=1080,
                scan_method="p"
            )
        ],
        video_term=[
            "x264",
            "8-bit"
        ],
    ),
    Metadata(
        audio_term=[
            "AAC"
        ],
        file_name="[TROLLORANGE] Hell Girl Season 4 (CR WEB-DL 1080p x264 AAC) | Hell Girl: Fourth Twilight | Jigoku Shoujo: Yoi no Togi",
        release_group=[
            "TROLLORANGE"
        ],
        series=[
            SeriesInfo(
                title="Hell Girl",
                season=[
                    SequenceNumber(
                        number=4
                    )
                ]
            ),
            SeriesInfo(
                title="Hell Girl: Fourth Twilight"
            ),
            SeriesInfo(
                title="Jigoku Shoujo: Yoi no Togi"
            )
        ],
        source=[
            "WEB-DL"
        ],
        video_resolution=[
            VideoResolution(
                video_height=1080,
                scan_method="p"
            )
        ],
        video_term=[
            "x264"
        ]
    ),
    Metadata(
        audio_term=[
            "FLAC",
            "Dual Audio"
        ],
        file_name="[Headpatter] Why Raeliana Ended Up at the Duke's Mansion Season 1 (BD Remux 1080p x264 8-bit FLAC [Dual Audio] | Kanojo ga Koushaku-tei ni Itta Riyuu",
        release_group=[
            "Headpatter"
        ],
        series=[
            SeriesInfo(
                title="Why Raeliana Ended Up at the Duke's Mansion",
                season=[
                    SequenceNumber(
                        number=1
                    )
                ]
            ),
            SeriesInfo(
                title="Kanojo ga Koushaku-tei ni Itta Riyuu"
            )
        ],
        release_information=[
            "Remux"
        ],
        source=[
            "BD"
        ],
        video_resolution=[
            VideoResolution(
                video_height=1080,
                scan_method="p"
            )
        ],
        video_term=[
            "x264",
            "8-bit"
        ]
    ),
    Metadata(
        audio_term=[
            "FLAC"
        ],
        file_name="[Moxie] We Never Learn: BOKUBEN S00E01-E02 (BD Remux 1080p x264 8-bit FLAC) | We Never Learn OVAs | Bokutachi wa Benkyou ga Dekinai OVAs",
        release_group=[
            "Moxie"
        ],
        series=[
            SeriesInfo(
                title="We Never Learn: BOKUBEN",
                season=[
                    SequenceNumber(
                        number=0
                    )
                ],
                episode=[
                    SequenceRange(
                        start=SequenceNumber(
                            number=1
                        ),
                        end=SequenceNumber(
                            number=2
                        )
                    )
                ]
            ),
            SeriesInfo(
                title="We Never Learn OVA"
            ),
            SeriesInfo(
                title="Bokutachi wa Benkyou ga Dekinai OVA"
            )
        ],
        release_information=[
            "Remux"
        ],
        source=[
            "BD"
        ],
        video_resolution=[
            VideoResolution(
                video_height=1080,
                scan_method="p"
            )
        ],
        video_term=[
            "x264",
            "8-bit"
        ]
    ),
    Metadata(
        file_name="[Furretar] 中文配 - 明日方舟 (Arknights) (Season 1-3) (Japanese + Mandarin Chinese Dub) (Matching Soft Subs) (Batch) [國語][国语][中文配音] (Prelude to Dawn) (Perish in Frost) (Rise from Ember) (Reimei Zensou) (Touin Kiro) (Enshin Shomei)",
        language=[
            "Japanese",
            "Mandarin",
            "Chinese"
        ],
        release_group=[
            "Furretar"
        ],
        release_information=[
            "Batch"
        ],
        series=[
            SeriesInfo(
                title="\u660e\u65e5\u65b9\u821f",
                season=[
                    SequenceRange(
                        start=SequenceNumber(
                            number=1
                        ),
                        end=SequenceNumber(
                            number=3
                        )
                    )
                ]
            )
        ],
        subs_term=[
            "Dub",
            "Soft Subs"
        ],
        unknown=[
            "Arknights",
            "Matching",
            "Prelude to Dawn",
            "Perish in Frost",
            "Rise from Ember",
            "Reimei Zensou",
            "Touin Kiro",
            "Enshin Shomei"
        ]
    ),
    Metadata(
        file_name="[Furretar] 台粤配 - 进击的巨人 (Attack on Titan) (Season 1-4 + Kanketsu-hen + OVA + Junior High) (Taiwanese Mandarin + Cantonese Chinese Dub) (Matching Soft Subs) [國語][粵語][国语][中配版] (進擊的巨人) (Shingeki no Kyojin) (The Last Attack) (Final Chapters)",
        language=[
            "Mandarin",
            "Cantonese",
            "Chinese"
        ],
        release_group=[
            "Furretar"
        ],
        series=[
            SeriesInfo(
                title="进击的巨人",
                season=[
                    SequenceRange(
                        start=SequenceNumber(
                            number=1
                        ),
                        end=SequenceNumber(
                            number=4
                        )
                    )
                ]
            )
        ],
        subs_term=[
            "Dub",
            "Soft Subs"
        ],
        unknown=[
            "Attack on Titan",
            "Kanketsu",
            "hen",
            "High",
            "Taiwanese",
            "Matching",
            "\u9032\u64ca\u7684\u5de8\u4eba",
            "Shingeki no Kyojin",
            "The Last Attack",
            "Chapters"
        ]
    )
]
