from aniparse.element import Metadata

table = [
    {
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01",
            Metadata.SEQUENCE_TITLE.value: "land of visible pain",
        },
        Metadata.FILE_NAME.value: "01 - land of visible pain"
    },

    {
        Metadata.SERIES_TITLE.value: {
            Metadata.MAIN.value: "5 centimeters per second"
        },
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_WIDTH.value: "1904",
            Metadata.VIDEO_HEIGHT.value: "1072"
        },
        Metadata.VIDEO_TERM.value: ["h264"],
        Metadata.AUDIO_TERM.value: ["flac"],
        Metadata.RELEASE_GROUP.value: "niizk",
        Metadata.FILE_NAME.value: "5_centimeters_per_second[1904x1072.h264.flac][niizk]"
    },
    {
        Metadata.SERIES_TITLE.value: "after war gundam x",
        Metadata.SEASON_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "1"
        },
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "03",
            Metadata.SEQUENCE_TITLE.value: "my mount is fierce!",
        },
        Metadata.FILE_NAME.value: "after war gundam x - 1x03 - my mount is fierce!"
    },
    {
        Metadata.SERIES_TITLE.value: "aim for the top! gunbuster",

        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_RANGE.value: "1"
        },
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_TERM.value: [
            "h264",
            "10bit"
        ],
        Metadata.AUDIO_TERM.value: "flac",
        Metadata.RELEASE_GROUP.value: "kaa",
        Metadata.FILE_CHECKSUM.value: "69eccdcf",
        Metadata.FILE_NAME.value: "aim_for_the_top!_gunbuster-ep1.bd(h264.flac.10bit)[kaa][69eccdcf]"
    },
    {
        Metadata.SERIES_TITLE.value: "attack on titan",
        Metadata.SEASON_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "3",
        },
        Metadata.FILE_NAME.value: "attack on titan season 3"
    },
    {
        Metadata.SERIES_TITLE.value: "attack on titan",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "3",
            Metadata.SEQUENCE_TITLE.value: "a dim light amid despair / humanity's comeback, part 1",
        },

        Metadata.FILE_NAME.value: "attack on titan - episode 3 - a dim light amid despair / humanity's comeback, part 1"
    },
    {
        Metadata.SERIES_TITLE.value: "bakemonogatari",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "3"
        },
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_WIDTH.value: "1280",
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.VIDEO_TERM.value: "avc",
        Metadata.AUDIO_TERM.value: ["aacx2"],
        Metadata.FILE_NAME.value: "bakemonogatari - 01 (bd 1280x720 avc aacx2)"
    },
    {
        Metadata.SERIES_TITLE.value: "chrono crusade",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: {
                Metadata.MAIN.value: [
                    {
                        Metadata.SEQUENCE_FROM.value: "1",
                        Metadata.SEQUENCE_TO.value: "5"
                    }
                ]
            }
        },
        Metadata.FILE_NAME.value: "chrono crusade ep. 1-5"
    },
    {
        Metadata.SERIES_TITLE.value: "cyborg 009",
        Metadata.SERIES_YEAR.value: "1968",
        Metadata.RELEASE_GROUP.value: "tshs",

        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "06",
        },

        Metadata.FILE_CHECKSUM.value: "30c15d62",
        Metadata.FILE_NAME.value: "cyborg 009 (1968) [tshs] episode 06 [30c15d62]"
    },
    {
        Metadata.SERIES_TITLE.value: "detective conan",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: {
                Metadata.MAIN.value: [
                    {
                        Metadata.SEQUENCE_FROM.value: "316",
                        Metadata.SEQUENCE_TO.value: "317"
                    }
                ]
            }
        },
        Metadata.RELEASE_GROUP.value: "dctp",
        Metadata.FILE_CHECKSUM.value: "2411959b",
        Metadata.FILE_NAME.value: "detective conan - 316-317 [dctp][2411959b]"
    },
    {
        Metadata.SERIES_TITLE.value: "dragon ball kai",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.VIDEO_TERM.value: [
            "x264"
        ],
        Metadata.SOURCE.value: "bluray",
        Metadata.RELEASE_GROUP.value: "dhd",
        Metadata.FILE_NAME.value: "dragon.ball.kai.-.01.-.1080p.bluray.x264.dhd"
    },
    {
        Metadata.SERIES_TITLE.value: "dragon ball z movies",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: {
                Metadata.MAIN.value: [
                    "8",
                    "10"
                ]
            }
        },
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.SOURCE.value: "bluray",
        Metadata.AUDIO_TERM.value: "dts",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.RELEASE_GROUP.value: "thora",
        Metadata.FILE_NAME.value: "dragon_ball_z_movies_8_&_10_[720p,bluray,dts,x264]_-_thora"
    },
    {
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01",
            Metadata.SERIES_TITLE.value: "the boy in the iceberg",
        },

        Metadata.FILE_NAME.value: "ep. 01 - the boy in the iceberg"
    },
    {
        Metadata.SERIES_TITLE.value: "evangelion shin gekijouban q",
        Metadata.SOURCE.value: "bdrip",
        Metadata.VIDEO_RESOLUTION.value: "1920x1080",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.AUDIO_TERM.value: [
            "flacx2",
            "5.1ch"
        ],
        Metadata.RELEASE_GROUP.value: "ank",
        Metadata.FILE_NAME.value: "evangelion shin gekijouban q (bdrip 1920x1080 x264 flacx2 5.1ch)-ank"
    },
    {
        Metadata.SERIES_TITLE.value: "evangelion the new movie q",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_WIDTH.value: "1280",
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.VIDEO_TERM.value: "avc",
        Metadata.AUDIO_TERM.value: [
            "aacx2",
            "5.1",
            "2.0"
        ],
        Metadata.FILE_NAME.value: "evangelion the new movie q (bd 1280x720 avc aacx2 [5.1+2.0])"
    },
    {
        Metadata.SERIES_TITLE.value: "eve no jikan 2",
        Metadata.FILE_CHECKSUM.value: "88f4f7f0",
        Metadata.FILE_NAME.value: "eve no jikan 2 [88f4f7f0]"
    },
    {
        Metadata.UNKNOWN.value: "evobot",
        Metadata.RELEASE_GROUP.value: "watakushi",
        Metadata.SERIES_TITLE.value: "akuma no riddle",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01"
        },
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.FILE_CHECKSUM.value: "69a307a2",
        Metadata.FILE_NAME.value: "evobot.[watakushi]_akuma_no_riddle_-_01v2_[720p][69a307a2]"
    },
    {
        Metadata.SERIES_TITLE.value: "fairy tail",
        Metadata.SEASON_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "06"
        },
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: {
                Metadata.MAIN.value: "32",
                Metadata.ALT.value: ["83"]
            },
            Metadata.SEQUENCE_TITLE.value: "tartaros arc iron fist of the fire dragon",
        },
        Metadata.FILE_NAME.value: "fairy tail - s06e32 - tartaros arc iron fist of the fire dragon [episode 83]"
    },
    {
        Metadata.SERIES_TITLE.value: "fate stay night",

        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "05",
            Metadata.SEQUENCE_TITLE.value: "the two magi part 1"
        },
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.SOURCE.value: "bluray",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.RELEASE_GROUP.value: "thora",
        Metadata.FILE_NAME.value: "fate_stay_night_ep05_the_two_magi_part1_[720p,bluray,x264]_-_thora"
    },
    {
        Metadata.SERIES_TITLE.value: "code geass r2",
        Metadata.SERIES_TYPE.value: "tv",

        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: {
                Metadata.SEQUENCE_NUMBER.value: "20",
                Metadata.SEQUENCE_TOTAL.value: "25"
            }
        },
        Metadata.LANGUAGE.value: [
            "ru",
            "jp",
            "ru"
        ],
        Metadata.SOURCE.value: "hdtv",
        Metadata.RELEASE_GROUP.value: ["varies & cuba77 & animereactor"],
        Metadata.FILE_NAME.value: "code_geass_r2_tv_[20_of_25]_[ru_jp]_[hdtv]_[varies_&_cuba77_&_animereactor_ru]"
    },
    {
        Metadata.SERIES_TITLE.value: "dramatical murder",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "1",
            Metadata.SEQUENCE_TITLE.value: "data 01 login"
        },
        Metadata.FILE_NAME.value: "dramatical murder episode 1 - data_01_login"
    },
    {
        Metadata.SERIES_TITLE.value: "evangelion 1.0 you are [not] alone",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.RELEASE_GROUP.value: "@home",
        Metadata.FILE_NAME.value: "evangelion_1.0_you_are_[not]_alone_(1080p)_[@home]"
    },
    {
        Metadata.SERIES_TITLE.value: "evangelion 1.11 you are (not) alone",
        Metadata.SERIES_YEAR.value: "2009",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.SOURCE.value: "bluray",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.AUDIO_TERM.value: "dts-es",
        Metadata.RELEASE_GROUP.value: "thora",
        Metadata.FILE_NAME.value: "evangelion_1.11_you_are_(not)_alone_(2009)_[1080p,bluray,x264,dts-es]_-_thora"
    },
    {
        Metadata.SERIES_TITLE.value: "fate stay night",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "05",
            Metadata.SEQUENCE_TITLE.value: "the two magi part 1"
        },
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.SOURCE.value: "bluray",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.RELEASE_GROUP.value: "thora",
        Metadata.FILE_NAME.value: "fate_stay_night_ep05_the_two_magi_part1_[720p,bluray,x264]_-_thora"
    },
    {
        Metadata.SERIES_TITLE.value: "gekkan shoujo nozaki-kun",
        Metadata.RELEASE_GROUP.value: "horriblesubs",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.FILE_NAME.value: "gekkan shoujo nozaki-kun [horriblesubs] (1080p)"
    },
    {
        Metadata.SERIES_TITLE.value: "ghost in the shell stand alone complex 2nd gig",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "05",
            Metadata.SEQUENCE_TITLE.value: "excavation"
        },
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.SOURCE.value: "hdtv",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.AUDIO_TERM.value: [
            "aac",
            "5.1"
        ],
        Metadata.RELEASE_GROUP.value: "thora",
        Metadata.FILE_NAME.value: "ghost_in_the_shell_stand_alone_complex_2nd_gig_ep05v2_excavation_[720p,hdtv,x264,aac_5.1]_-_thora"
    },
    {
        Metadata.SERIES_TITLE.value: "gin'iro no kami no agito",
        Metadata.SERIES_YEAR.value: "2006",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.SOURCE.value: "bluray",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.AUDIO_TERM.value: "dts",
        Metadata.RELEASE_GROUP.value: "thora",
        Metadata.FILE_NAME.value: "gin'iro_no_kami_no_agito_(2006)_[1080p,bluray,x264,dts]_-_thora"
    },
    {
        Metadata.SERIES_TITLE.value: "hayate no gotoku",
        Metadata.SEASON_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "2"
        },
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "24"
        },
        Metadata.SOURCE.value: "blu-ray",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.RELEASE_GROUP.value: "chihiro",
        Metadata.FILE_NAME.value: "hayate no gotoku 2nd season 24 (blu-ray 1080p) [chihiro]"
    },
    {
        Metadata.SERIES_TITLE.value: "howl's moving castle",
        Metadata.SERIES_YEAR.value: "2004",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.SOURCE.value: "bluray",
        Metadata.AUDIO_TERM.value: [
            "flac",
            "dts"
        ],
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.RELEASE_GROUP.value: "thora",
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.FILE_NAME.value: "howl's_moving_castle_(2004)_[1080p,bluray,flac,dts,x264]_-_thora v2"
    },
    {
        Metadata.SERIES_TITLE.value: "juuni kokki",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "5"
        },
        Metadata.FILE_NAME.value: "juuni kokki ep.5"
    },
    {
        Metadata.SERIES_TITLE.value: "juuousei",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01"
        },
        Metadata.RELEASE_GROUP.value: "black_sheep",
        Metadata.SOURCE.value: "hdtv",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "803da487",
        Metadata.FILE_NAME.value: "juuousei_-_01_[black_sheep][hdtv_h264_aac][803da487]"
    },
    {
        Metadata.SERIES_TITLE.value: "k-on!!",

        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "08",
            Metadata.SEQUENCE_TITLE.value: "career plan!"
        },
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.SOURCE.value: "bluray",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.RELEASE_GROUP.value: "thora",
        Metadata.FILE_NAME.value: "k-on!!_ep08_career_plan!_[1080p,bluray,x264]_-_thora"
    },
    {
        Metadata.SERIES_TITLE.value: "kotonoha no niwa",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720",
            Metadata.VIDEO_WIDTH.value: "1280"
        },
        Metadata.VIDEO_TERM.value: "avc",
        Metadata.AUDIO_TERM.value: [
            "aacx3",
            "5.1",
            "2.0",
            "2.0"
        ],
        Metadata.SUBS_TERM.value: "subx3",
        Metadata.FILE_NAME.value: "kotonoha no niwa (bd 1280x720 avc aacx3 [5.1+2.0+2.0] subx3)"
    },
    {
        Metadata.SERIES_TITLE.value: "macross frontier - sayonara no tsubasa",
        Metadata.SOURCE.value: "central anime",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.FILE_CHECKSUM.value: "46b35e25",
        Metadata.FILE_NAME.value: "macross frontier - sayonara no tsubasa (central anime, 720p) [46b35e25]"
    },
    {
        Metadata.SERIES_TITLE.value: "magical girl lyrical nanoha a's",
        Metadata.EPISODE_PREFIX.value: {Metadata.SEQUENCE_NUMBER.value: "01"},
        Metadata.SOURCE.value: "dvd",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.RELEASE_GROUP.value: "dgz",
        Metadata.FILE_CHECKSUM.value: "7a8a7769",
        Metadata.FILE_NAME.value: "magical girl lyrical nanoha a's - 01.dvd[h264.aac][dgz][7a8a7769]"
    },
    {
        Metadata.SERIES_TITLE.value: "mary bell",
        Metadata.SOURCE.value: "dvd",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01"
        },
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.RELEASE_GROUP.value: "h-b",
        Metadata.FILE_NAME.value: "mary bell (dvd) - 01v2 [h-b]"
    },
    {
        Metadata.SERIES_TITLE.value: "mobile suit gundam 00",
        Metadata.SEASON_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "2"
        },
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "07",
            Metadata.SEQUENCE_TITLE.value: "a reunion and a parting"
        },

        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.SOURCE.value: "bluray",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.RELEASE_GROUP.value: "thora",
        Metadata.FILE_NAME.value: "mobile_suit_gundam_00_season_2_ep07_a_reunion_and_a_parting_[1080p,bluray,x264]_-_thora"
    },
    {
        Metadata.SERIES_TITLE.value: "neko no ongaeshi",
        Metadata.RELEASE_GROUP.value: "hqr",
        Metadata.RELEASE_INFORMATION.value: "remux",
        Metadata.AUDIO_TERM.value: "dualaudio",
        Metadata.SOURCE.value: "ntv",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "692",
            Metadata.VIDEO_WIDTH.value: "1280"
        },
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.FILE_CHECKSUM.value: "0cdc2145",
        Metadata.FILE_NAME.value: "neko no ongaeshi - [hqr.remux-dualaudio][ntv.1280x692.h264](0cdc2145)"
    },
    {
        Metadata.SERIES_TITLE.value: "noein",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: {
                Metadata.MAIN.value: {
                    Metadata.SEQUENCE_NUMBER.value: "01",
                    Metadata.SEQUENCE_TOTAL.value: "24"
                }
            }
        },
        Metadata.LANGUAGE.value: [
            "ru",
            "jp"
        ],
        Metadata.RELEASE_GROUP.value: "bodlerov & torrents ru",
        Metadata.FILE_NAME.value: "noein_[01_of_24]_[ru_jp]_[bodlerov_&_torrents_ru]"
    },
    {
        Metadata.SERIES_TITLE.value: "noragami",
        Metadata.SEASON_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "02"
        },

        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "06",
            Metadata.SEQUENCE_TITLE.value: "what must be done"
        },
        Metadata.FILE_NAME.value: "noragami - s02e06 - what must be done [episode 6]"
    },
    {
        Metadata.SERIES_TITLE.value: "ookiku furikabutte",
        Metadata.SEASON_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "2"
        },
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "09"
        },
        Metadata.RELEASE_GROUP.value: "central anime",
        Metadata.FILE_CHECKSUM.value: "bd841253",
        Metadata.FILE_NAME.value: "ookiku furikabutte s2 - 09 (central anime) [bd841253]"
    },
    {
        Metadata.SERIES_TITLE.value: "queen's blade utsukushiki toushi-tachi",
        Metadata.SERIES_TYPE.value: "ova",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01"
        },
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720",
            Metadata.VIDEO_WIDTH.value: "1280"
        },
        Metadata.VIDEO_TERM.value: "avc",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_NAME.value: "queen's blade utsukushiki toushi-tachi - ova_01 (bd 1280x720 avc aac)"
    },
    {
        Metadata.SERIES_TITLE.value: "the irregular at magic high school",
        Metadata.SEASON_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01"
        },
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01",
            Metadata.SEQUENCE_TITLE.value: "enrollment part i"
        },
        Metadata.FILE_NAME.value: "the irregular at magic high school - s01e01- enrollment part i"
    },
    {
        Metadata.SERIES_TITLE.value: "the idolm@ster 765 pro to iu monogatari",
        Metadata.FILE_NAME.value: "the idolm@ster 765 pro to iu monogatari"
    },
    {
        Metadata.SERIES_TITLE.value: "to aru kagaku no railgun",
        Metadata.EPISODE_PREFIX.value: [
            "13",
            "15"
        ],
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.RELEASE_GROUP.value: "atsa",
        Metadata.FILE_NAME.value: "to_aru_kagaku_no_railgun_13-15_[bd_1080p][atsa]"
    },
    {
        Metadata.SERIES_TITLE.value: "toradora! asdwd",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "03",
            Metadata.SEQUENCE_TITLE.value: "your-song"
        },
        Metadata.FILE_NAME.value: "toradora! asdwd-03-your-song"
    },
    {
        Metadata.SERIES_TITLE.value: "toradora!",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "03",
            Metadata.SEQUENCE_TITLE.value: "your-song"
        },
        Metadata.FILE_NAME.value: "toradora-e03-your-song"
    },
    {
        Metadata.SERIES_TITLE.value: "toradora!",
        Metadata.SEASON_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01",
        },
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "03",
            Metadata.SEQUENCE_TITLE.value: "your song"
        },
        Metadata.FILE_NAME.value: "toradora! s01e03-your song"
    },
    {
        Metadata.SERIES_TITLE.value: "tsuredure children",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "1",
            Metadata.SEQUENCE_TITLE.value: "confession"
        },
        Metadata.FILE_NAME.value: "tsuredure children epis\u00f3dio 1 \u2013 confession"
    },
    {
        Metadata.VOLUME_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01"
        },
        Metadata.FILE_NAME.value: "vol.01"
    },
    {
        Metadata.RELEASE_GROUP.value: "(\u00b4\u2022 \u03c9 \u2022`)",
        Metadata.SERIES_TITLE.value: "nintama rantarou",
        Metadata.SEASON_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "23"
        },
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "1821",
            Metadata.SEQUENCE_TITLE.value: "buddhist priest-sama is a ninja"
        },
        Metadata.FILE_NAME.value: "[(\u00b4\u2022 \u03c9 \u2022`)] nintama rantarou - s23e1821 - buddhist priest-sama is a ninja"
    },
    {
        Metadata.RELEASE_GROUP.value: "0x539",
        Metadata.SERIES_TITLE.value: "somali and the forest spirit",
        Metadata.SEASON_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01"
        },
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01"
        },
        Metadata.SOURCE.value: "web",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.VIDEO_TERM.value: "hi10p",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "bb7c6531",
        Metadata.FILE_NAME.value: "[0x539] somali and the forest spirit - s01e01 (web 1080p hi10p aac) [bb7c6531]"
    },
    {
        Metadata.RELEASE_GROUP.value: "46620",
        Metadata.SERIES_TITLE.value: "re:zero kara hajimeru isekai seikatsu",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.VIDEO_TERM.value: "av1",
        Metadata.FILE_NAME.value: "[46620] re:zero kara hajimeru isekai seikatsu [1080p av1]"
    },
    {
        Metadata.RELEASE_GROUP.value: "5f",
        Metadata.SERIES_TITLE.value: "rwby",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "14",
            Metadata.SEQUENCE_TITLE.value: "forever fall part 2"
        },
        Metadata.LANGUAGE.value: [
            "pt-br"
        ],
        Metadata.FILE_NAME.value: "[5f] rwby - 14 forever fall part 2 pt-br"
    },
    {
        Metadata.RELEASE_GROUP.value: "acxsaintdeath",
        Metadata.SERIES_TITLE.value: "neon genesis evangelion - platinum",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "06",
            Metadata.SEQUENCE_TITLE.value: "showdown in tokyo 3"
        },
        Metadata.FILE_CHECKSUM.value: "cbdb8577",
        Metadata.FILE_NAME.value: "[acx]neon_genesis_evangelion_-_platinum_-_06_-_showdown_in_tokyo_3_[saintdeath]_[cbdb8577]"
    },
    {
        Metadata.RELEASE_GROUP.value: "akh-swe",
        Metadata.SERIES_TITLE.value: "fullmetal alchemist",
        Metadata.SERIES_YEAR.value: "2009",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "02"
        },
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.VIDEO_TERM.value: "h.264",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "7b2c5e8b",
        Metadata.FILE_NAME.value: "[akh-swe]_fullmetal_alchemist_(2009)_02v2_[h.264.aac][7b2c5e8b]"
    },
    {
        Metadata.RELEASE_GROUP.value: "anbu-menclave",
        Metadata.SERIES_TITLE.value: "canaan",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01"
        },
        Metadata.VIDEO_RESOLUTION.value: "1024x576",
        Metadata.VIDEO_TERM.value: "h.264",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "12f00e89",
        Metadata.FILE_NAME.value: "[anbu-menclave]_canaan_-_01_[1024x576_h.264_aac][12f00e89]"
    },
    {
        Metadata.RELEASE_GROUP.value: "anbu-umai",
        Metadata.SERIES_TITLE.value: "haiyoru! nyaru-ani",
        Metadata.FILE_CHECKSUM.value: "596dd8e6",
        Metadata.FILE_NAME.value: "[anbu-umai]_haiyoru!_nyaru-ani_[596dd8e6]"
    },
    {
        Metadata.RELEASE_GROUP.value: "anbu",
        Metadata.SERIES_TITLE.value: "princess lover!",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.FILE_CHECKSUM.value: "2048a39a",
        Metadata.FILE_NAME.value: "[anbu]_princess_lover!_-_01_[2048a39a]"
    },
    {
        Metadata.RELEASE_GROUP.value: "animerg",
        Metadata.SERIES_TITLE.value: {
            Metadata.MAIN.value: "shingeki no kyojin (the final season)",
            Metadata.ALT.value: ["attack on titan"]
        },
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: {
                Metadata.MAIN.value: "13",
                Metadata.ALT.value: "72"
            }
        },
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.VIDEO_TERM.value: "10bit",
        Metadata.AUDIO_TERM.value: "dual audio",
        Metadata.FILE_NAME.value: "[animerg] shingeki no kyojin (the final season) - 13 [1080p 10bit dual audio] (attack on titan - 72)"
    },
    {
        Metadata.RELEASE_GROUP.value: "animergxcelent",
        Metadata.SERIES_TITLE.value: "ushio to tora ",
        Metadata.SERIES_TYPE.value: "tv",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "02"
        },
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720",
        },
        Metadata.FILE_NAME.value: "[animerg] ushio to tora (tv) - 02 [720p] [xcelent]"
    },

    {
        Metadata.RELEASE_GROUP.value: "aojiaozero",
        Metadata.SERIES_TITLE.value: "mangaka-san to assistant-san to the animation",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "02"
        },
        Metadata.UNKNOWN.value: "big",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.FILE_NAME.value: "[aojiaozero][mangaka-san to assistant-san to the animation] ep02 [big][x264_aac][720p]"
    },
    {
        Metadata.RELEASE_GROUP.value: "ayako",
        Metadata.SERIES_TITLE.value: "infinite stratos - is",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01"
        },
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.VIDEO_TERM.value: "xvid",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_WIDTH.value: "480"
        },
        Metadata.FILE_CHECKSUM.value: "29675b71",
        Metadata.FILE_NAME.value: "[ayako]_infinite_stratos_-_is_-_01v2_[xvid][400p][29675b71]"
    },
    {
        Metadata.RELEASE_GROUP.value: "ayu",
        Metadata.SERIES_TITLE.value: "kiddy grade 2 - pilot",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.AUDIO_TERM.value: "ac3",
        Metadata.FILE_CHECKSUM.value: "650b731b",
        Metadata.FILE_NAME.value: "[ayu]_kiddy_grade_2_-_pilot_[h264_ac3][650b731b]"
    },
    {
        Metadata.RELEASE_GROUP.value: "b-g_&_m.3.3.w",
        Metadata.SERIES_TITLE.value: "myself yourself",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "12"
        },
        Metadata.SOURCE.value: "dvd",
        Metadata.VIDEO_TERM.value: "h.264",
        Metadata.AUDIO_TERM.value: "dd2.0",
        Metadata.FILE_CHECKSUM.value: "cb2b37f1",
        Metadata.FILE_NAME.value: "[b-g_&_m.3.3.w]_myself_yourself_12.dvd(h.264_dd2.0)_[cb2b37f1]"
    },
    {
        Metadata.RELEASE_GROUP.value: "bm&t",
        Metadata.SERIES_TITLE.value: "toradora!",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "07",
            Metadata.SEQUENCE_TITLE.value: "pool opening"
        },
        Metadata.RELEASE_VERSION.value: "2",

        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.VIDEO_TERM.value: "hi10",
        Metadata.SOURCE.value: "bd",
        Metadata.FILE_CHECKSUM.value: "8f59f2ba",
        Metadata.FILE_NAME.value: "[bm&t] toradora! - 07v2 - pool opening [720p hi10 ] [bd] [8f59f2ba]"
    },
    {
        Metadata.RELEASE_GROUP.value: "bakawolf-m.3.3.w",
        Metadata.SERIES_TITLE.value: "special a",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01"
        },
        Metadata.VIDEO_TERM.value: "h.264",
        Metadata.FILE_CHECKSUM.value: "c83164b9",
        Metadata.FILE_NAME.value: "[bakawolf-m.3.3.w] special a 01 (h.264) [c83164b9]"
    },
    {
        Metadata.RELEASE_GROUP.value: "bludragon",
        Metadata.SERIES_TITLE.value: "blue submarine no.6",
        Metadata.SOURCE.value: "dvd",
        Metadata.UNKNOWN.value: "r2",
        Metadata.AUDIO_TERM.value: "dual audio",
        Metadata.RELEASE_VERSION.value: "3",
        Metadata.FILE_NAME.value: "[bludragon] blue submarine no.6 (dvd, r2, dual audio) v3"
    },
    {
        Metadata.RELEASE_GROUP.value: "ch",
        Metadata.SERIES_TITLE.value: "sword art online extra edition",
        Metadata.AUDIO_TERM.value: "dual audio",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "480"
        },
        Metadata.VIDEO_TERM.value: [
            "10bit",
            "h.264",
            "vorbis"
        ],
        Metadata.FILE_NAME.value: "[ch] sword art online extra edition dual audio [bd 480p][10bith.264vorbis]"
    },
    {
        Metadata.RELEASE_GROUP.value: "cms",
        Metadata.SERIES_TITLE.value: "magical\u2606star kanon 100%",
        Metadata.SERIES_TYPE.value: "OVA",
        Metadata.SOURCE.value: "DVD",
        Metadata.FILE_CHECKSUM.value: "e9f43685",
        Metadata.FILE_NAME.value: "[cms] magical\u2606star kanon 100% OVA[DVD][e9f43685]"
    },
    {
        Metadata.RELEASE_GROUP.value: "chihiro",
        Metadata.SERIES_TITLE.value: "kono aozora ni yakusoku wo",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "10"
        },
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.SOURCE.value: "dvd",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.FILE_CHECKSUM.value: "c83d206b",
        Metadata.FILE_NAME.value: "[chihiro]_kono_aozora_ni_yakusoku_wo_10_v2_[dvd][h264][c83d206b]"
    },

    {
        Metadata.RELEASE_GROUP.value: "coalgirls",
        Metadata.SERIES_TITLE.value: "fate zero",
        Metadata.SERIES_TYPE.value: "ova",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "3.5"
        },
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_WIDTH.value: "1280",
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.SOURCE.value: "blu-ray",
        Metadata.AUDIO_TERM.value: "flac",
        Metadata.FILE_CHECKSUM.value: "5f5ad026",
        Metadata.FILE_NAME.value: "[coalgirls]_fate_zero_ova3.5_(1280x720_blu-ray_flac)_[5f5ad026]"
    },

    {
        Metadata.RELEASE_GROUP.value: "coalgirls",
        Metadata.SERIES_TITLE.value: "white album",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: {
                Metadata.SEQUENCE_FROM.value: "1",
                Metadata.SEQUENCE_TO.value: "13"
            }
        },
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_WIDTH.value: "1280",
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.SOURCE.value: "blu-ray",
        Metadata.AUDIO_TERM.value: "flac",
        Metadata.FILE_NAME.value: "[coalgirls]_white_album_1-13_(1280\u00d7720_blu-ray_flac)"
    },
    {
        Metadata.RELEASE_GROUP.value: "Commie",
        Metadata.SERIES_TITLE.value: "Last Exile ~fam, the silver wing~",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "13"
        },
        Metadata.FILE_CHECKSUM.value: "aff9e530",
        Metadata.FILE_NAME.value: "[Commie] Last Exile ~fam, the silver wing~ - 13 [aff9e530]"
    },
    {
        Metadata.RELEASE_GROUP.value: "conclave-mendoi",
        Metadata.SERIES_TITLE.value: "mobile suit gundam 00",
        Metadata.SEASON_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "2"
        },
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01"
        },
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_WIDTH.value: "1280",
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.VIDEO_TERM.value: "h.264",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "4863fbe8",
        Metadata.FILE_NAME.value: "[conclave-mendoi]_mobile_suit_gundam_00_s2_-_01v2_[1280x720_h.264_aac][4863fbe8]"
    },
    {
        Metadata.RELEASE_GROUP.value: "db",
        Metadata.SERIES_TITLE.value: "bleach",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "225"
        },
        Metadata.FILE_CHECKSUM.value: "c63d149c",
        Metadata.FILE_NAME.value: "[db]_bleach_225_[c63d149c]"
    },
    {
        Metadata.RELEASE_GROUP.value: "darksoul-subs",
        Metadata.SERIES_TITLE.value: "tatakau shisho - the book of bantorra",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_WIDTH.value: "848",
            Metadata.VIDEO_HEIGHT.value: "480"
        },
        Metadata.VIDEO_TERM.value: "xvid",
        Metadata.AUDIO_TERM.value: "mp3",
        Metadata.FILE_NAME.value: "[darksoul-subs] tatakau shisho - the book of bantorra [848x480 xvid_mp3]"
    },
    {
        Metadata.RELEASE_GROUP.value: "dmonhiro",
        Metadata.SERIES_TITLE.value: "magi - the labyrinth of magic",
        Metadata.VOLUME_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "1"
        },
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.FILE_NAME.value: "[dmonhiro] magi - the labyrinth of magic - vol.1v2 (bd, 720p)"
    },
    {
        Metadata.RELEASE_GROUP.value: "dmonhiro",
        Metadata.SERIES_TITLE.value: "oreshura",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01",
            Metadata.SEQUENCE_TITLE.value: "the start of high school life is a war zone"
        },
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.FILE_CHECKSUM.value: "211375e6",
        Metadata.FILE_NAME.value: "[dmonhiro] oreshura #01v2 - the start of high school life is a war zone [bd, 720p] [211375e6]"
    },
    {
        Metadata.RELEASE_GROUP.value: "doki",
        Metadata.SERIES_TITLE.value: "nogizaka haruka no himitsu - purezza",
        Metadata.EPISODE_PREFIX.value: [
            "01",
            "03"
        ],
        Metadata.RELEASE_VERSION.value: [
            "2",
            "2"
        ],
        "range_separator": "-",
        Metadata.VIDEO_RESOLUTION.value: "1280x720",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_NAME.value: "[doki] nogizaka haruka no himitsu - purezza - 01v2-03v2 (1280x720 h264 aac)"
    },
    {
        Metadata.RELEASE_GROUP.value: "doremi",
        Metadata.SERIES_TITLE.value: "ro-kyu-bu! ss",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.FILE_CHECKSUM.value: "c1b5ce5d",
        Metadata.FILE_NAME.value: "[doremi].ro-kyu-bu!.ss.01.[c1b5ce5d]"
    },
    {
        Metadata.RELEASE_GROUP.value: "dragsterps",
        Metadata.SERIES_TITLE.value: "devilman crybaby",
        Metadata.SEASON_PREFIX.value: "s",
        Metadata.SEASON_PREFIX.value: "01",
        Metadata.EPISODE_PREFIX.value: "e",
        Metadata.EPISODE_PREFIX.value: "04",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.AUDIO_TERM.value: "multi-audio",
        Metadata.SUBS_TERM.value: "multi-subs",
        Metadata.FILE_CHECKSUM.value: "24b349d4",
        Metadata.FILE_NAME.value: "[dragsterps] devilman crybaby s01e04 [720p] [multi-audio] [multi-subs] [24b349d4]"
    },
    {
        Metadata.RELEASE_GROUP.value: "e-haro raws",
        Metadata.SERIES_TITLE.value: "kore wa zombie desu ka",
        Metadata.EPISODE_PREFIX.value: "03",
        Metadata.SERIES_TYPE.value: "tv",
        Metadata.VIDEO_RESOLUTION.value: "1280x720",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "888e4991",
        Metadata.FILE_NAME.value: "[e-haro raws] kore wa zombie desu ka - 03 (tv 1280x720 h264 aac) [888e4991]"
    },
    {
        Metadata.RELEASE_GROUP.value: "edomae subs",
        Metadata.SERIES_TITLE.value: "kore wa zombie desu ka",
        Metadata.EPISODE_PREFIX.value: "episode",
        Metadata.EPISODE_PREFIX.value: "2",
        Metadata.FILE_NAME.value: "[edomae subs] kore wa zombie desu ka  episode 2"
    },
    {
        Metadata.RELEASE_GROUP.value: "elysium",
        Metadata.SERIES_TITLE.value: "sora no woto",
        Metadata.EPISODE_PREFIX.value: "ep",
        Metadata.EPISODE_PREFIX.value: "07.5",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "c37580f8",
        Metadata.FILE_NAME.value: "[elysium]sora.no.woto.ep07.5(bd.720p.aac)[c37580f8]"
    },
    {
        Metadata.RELEASE_GROUP.value: "ember",
        Metadata.SERIES_TITLE.value: "natsu no arashi!",
        Metadata.SEASON_PREFIX.value: "s",
        Metadata.SEASON_PREFIX.value: "01",
        Metadata.EPISODE_PREFIX.value: "e",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.EPISODE_PREFIX.value: "playback part 2",
        Metadata.FILE_CHECKSUM.value: "bd00f464",
        Metadata.FILE_NAME.value: "[ember] natsu no arashi! - s01e01-playback part 2 [bd00f464]"
    },
    {
        Metadata.RELEASE_GROUP.value: "erai-raws",
        Metadata.SERIES_TITLE.value: "one piece",
        Metadata.EPISODE_PREFIX.value: "1000",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.SUBS_TERM.value: "multiple subtitle",
        Metadata.FILE_CHECKSUM.value: "f2ae5ff6",
        Metadata.FILE_NAME.value: "[erai-raws] one piece - 1000 [1080p][multiple subtitle][f2ae5ff6]"
    },
    {
        Metadata.RELEASE_GROUP.value: "erogaki-team",
        Metadata.SERIES_TITLE.value: "nurse witch komugi-chan magikarte",
        Metadata.EPISODE_PREFIX.value: "02.5",
        Metadata.FILE_CHECKSUM.value: "902bb314",
        Metadata.FILE_NAME.value: "[erogaki-team]_nurse_witch_komugi-chan_magikarte_02.5_[902bb314]"
    },
    {
        Metadata.RELEASE_GROUP.value: "evetaku",
        Metadata.SERIES_TITLE.value: "akb0048",
        Metadata.VOLUME_PREFIX.value: "vol",
        "volume_number": "03",
        Metadata.EPISODE_PREFIX.value: "making of kibou-ni-tsuite music video",
        Metadata.VIDEO_TERM.value: [
            "bdrip",
            "h.264",
            "hi10p"
        ],
        Metadata.VIDEO_RESOLUTION.value: "1080i",
        Metadata.AUDIO_TERM.value: "flac",
        Metadata.FILE_CHECKSUM.value: "c09462e2",
        Metadata.FILE_NAME.value: "[evetaku] akb0048 vol.03 - making of kibou-ni-tsuite music video (bdrip 1080i h.264-hi10p flac)[c09462e2]"
    },
    {
        Metadata.RELEASE_GROUP.value: "fbi",
        Metadata.SERIES_TITLE.value: "baby princess 3d paradise love",
        Metadata.EPISODE_PREFIX.value: "01",
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "0",
        Metadata.VIDEO_TERM.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "457cc066",
        Metadata.FILE_NAME.value: "[fbi] baby princess 3d paradise love 01v0 [bd][720p-aac][457cc066]"
    },
    {
        Metadata.RELEASE_GROUP.value: "deep",
        Metadata.SERIES_TITLE.value: "tegami bachi (reverse) - letter bee",
        Metadata.EPISODE_PREFIX.value: "29",
        "episode_number_alt": "04",
        Metadata.FILE_CHECKSUM.value: "5203142b",
        Metadata.FILE_NAME.value: "[deep] tegami bachi (reverse) - letter bee - 29 (04) [5203142b]"
    },
    {
        Metadata.RELEASE_GROUP.value: "fb",
        Metadata.SERIES_TITLE.value: "crayon shin-chan",
        Metadata.SERIES_TYPE.value: "movie",
        Metadata.EPISODE_PREFIX.value: "2",
        Metadata.EPISODE_PREFIX.value: "the secret of buri buri kingdom",
        Metadata.VIDEO_TERM.value: "divx5",
        Metadata.AUDIO_TERM.value: "ac3",
        Metadata.SERIES_YEAR.value: "1994",
        Metadata.VIDEO_RESOLUTION.value: "852x480",
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.FILE_NAME.value: "[fb] crayon shin-chan movie 2 the secret of buri buri kingdom [divx5 ac3] 1994 [852x480] v2"
    },
    {
        Metadata.RELEASE_GROUP.value: "fff",
        Metadata.SERIES_TITLE.value: "futsuu no joshikousei ga [locodol] yatte mita.",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.FILE_CHECKSUM.value: "bad09c76",
        Metadata.FILE_NAME.value: "[fff] futsuu no joshikousei ga [locodol] yatte mita. - 01 [bad09c76]"
    },

    {
        Metadata.RELEASE_GROUP.value: "fff",
        Metadata.SERIES_TITLE.value: "red data girl",
        Metadata.EPISODE_PREFIX.value: "10",
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "0",
        Metadata.FILE_CHECKSUM.value: "29ea865b",
        Metadata.FILE_NAME.value: "[fff] red data girl - 10v0 [29ea865b]"
    },
    {
        Metadata.RELEASE_GROUP.value: "fff",
        Metadata.SERIES_TITLE.value: "seirei tsukai no blade dance",
        Metadata.SERIES_TYPE.value: "sp",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "f1ff8588",
        Metadata.FILE_NAME.value: "[fff] seirei tsukai no blade dance - sp01 [bd][720p-aac][f1ff8588]"
    },
    {
        Metadata.RELEASE_GROUP.value: "faggotryraws",
        Metadata.SERIES_TITLE.value: "bakuman",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.SOURCE.value: "nhk e",
        Metadata.VIDEO_RESOLUTION.value: "848x480",
        Metadata.FILE_NAME.value: "[faggotryraws] bakuman - 01 (nhk e 848x480)"
    },
    {
        Metadata.RELEASE_GROUP.value: "frostii",
        Metadata.SERIES_TITLE.value: "nodame cantabile finale",
        Metadata.EPISODE_PREFIX.value: "00",
        Metadata.FILE_CHECKSUM.value: "73ad0735",
        Metadata.FILE_NAME.value: "[frostii]_nodame_cantabile_finale_-_00_[73ad0735]"
    },
    {
        Metadata.RELEASE_GROUP.value: "gs",
        Metadata.SERIES_TITLE.value: "classroom crisis",
        Metadata.VOLUME_PREFIX.value: "vol.",
        "volume_number": [
            "1",
            "2"
        ],
        "range_separator": "&",
        Metadata.VIDEO_TERM.value: [
            "bd",
            "10bit"
        ],
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.AUDIO_TERM.value: "flac",
        Metadata.FILE_NAME.value: "[gs] classroom crisis vol.1&2 (bd 1080p 10bit flac)"
    },
    {
        Metadata.RELEASE_GROUP.value: "grimripper",
        Metadata.SERIES_TITLE.value: "koi kaze",
        Metadata.AUDIO_TERM.value: "dual audio",
        Metadata.EPISODE_PREFIX.value: "ep",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.FILE_CHECKSUM.value: "c13cefe0",
        Metadata.FILE_NAME.value: "[grimripper] koi kaze [dual audio] ep01 (c13cefe0)"
    },
    {
        Metadata.RELEASE_GROUP.value: "hakata ramen",
        Metadata.SERIES_TITLE.value: "cells at work!",
        Metadata.SERIES_TYPE.value: "special",
        Metadata.FILE_NAME.value: "[hakata ramen] cells at work! special"
    },
    {
        Metadata.RELEASE_GROUP.value: "hakugetsu&mgrt",
        Metadata.SERIES_TITLE.value: "evangelion 3.0 you can (not) redo",
        Metadata.VIDEO_RESOLUTION.value: "480p",
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "0",
        Metadata.FILE_NAME.value: "[hakugetsu&mgrt][evangelion 3.0 you can (not) redo][480p][v0]"
    },
    {
        Metadata.RELEASE_GROUP.value: "hard-boiled fs",
        Metadata.SERIES_TITLE.value: "fullmetalalchemist",
        Metadata.EPISODE_PREFIX.value: "09",
        Metadata.FILE_NAME.value: "[hard-boiled fs]fullmetalalchemist_09"
    },
    {
        Metadata.RELEASE_GROUP.value: "harunatsu",
        Metadata.SERIES_TITLE.value: "classroom crisis",
        Metadata.VOLUME_PREFIX.value: "vol.",
        "volume_number": "1",
        Metadata.VIDEO_TERM.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_NAME.value: "[harunatsu] classroom crisis - vol.1 [bd 720p-aac]"
    },
    {
        Metadata.RELEASE_GROUP.value: "hatsuyuki-kaitou",
        Metadata.SERIES_TITLE.value: "fairy tail",
        Metadata.SEASON_PREFIX.value: "2",
        Metadata.EPISODE_PREFIX.value: "52",
        "episode_number_alt": "227",
        Metadata.VIDEO_TERM.value: [
            "720p",
            "10bit"
        ],
        Metadata.FILE_CHECKSUM.value: "9df6b8d5",
        Metadata.FILE_NAME.value: "[hatsuyuki-kaitou]_fairy_tail_2_-_52_(227)_[720p][10bit][9df6b8d5]"
    },
    {
        Metadata.RELEASE_GROUP.value: "hatsuyuki",
        Metadata.SERIES_TITLE.value: "dragon ball kai",
        Metadata.SERIES_YEAR.value: "2014",
        Metadata.EPISODE_PREFIX.value: "002",
        "episode_number_alt": "100",
        Metadata.VIDEO_RESOLUTION.value: "1280x720",
        Metadata.FILE_CHECKSUM.value: "dd66afb7",
        Metadata.FILE_NAME.value: "[hatsuyuki] dragon ball kai (2014) - 002 (100) [1280x720][dd66afb7]"
    },
    {
        Metadata.RELEASE_GROUP.value: "hatsuyuki",
        Metadata.SERIES_TITLE.value: "kuroko no basuke",
        Metadata.SEASON_PREFIX.value: "s",
        Metadata.SEASON_PREFIX.value: "3",
        Metadata.EPISODE_PREFIX.value: "01",
        "episode_number_alt": "51",
        Metadata.VIDEO_TERM.value: [
            "720p",
            "10bit"
        ],
        Metadata.FILE_CHECKSUM.value: "619c57a0",
        Metadata.FILE_NAME.value: "[hatsuyuki]_kuroko_no_basuke_s3_-_01_(51)_[720p][10bit][619c57a0]"
    },
    {
        Metadata.RELEASE_GROUP.value: "hien",
        Metadata.SERIES_TITLE.value: "kotoura-san - special short anime 'haruka's room'",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.VIDEO_TERM.value: [
            "h.264",
            "10-bit"
        ],
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "6b6be015",
        Metadata.FILE_NAME.value: "[hien] kotoura-san - special short anime 'haruka's room' - 01 [bd 1080p h.264 10-bit aac][6b6be015]"
    },
    {
        Metadata.RELEASE_GROUP.value: "himatsubushi",
        Metadata.SERIES_TITLE.value: "sora no woto",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.FILE_CHECKSUM.value: "e83ad672",
        Metadata.FILE_NAME.value: "[himatsubushi]_sora_no_woto_-_01_-_h264_-_720p_-_e83ad672"
    },
    {
        Metadata.RELEASE_GROUP.value: "hiryuu",
        Metadata.SERIES_TITLE.value: "maji de watashi ni koi shinasai!!",
        Metadata.EPISODE_PREFIX.value: "02",
        Metadata.VIDEO_TERM.value: "720",
        Metadata.FILE_NAME.value: "[hiryuu] maji de watashi ni koi shinasai!! - 02 [720]"
    },
    {
        Metadata.RELEASE_GROUP.value: "horriblesubs",
        Metadata.SERIES_TITLE.value: "gintama",
        Metadata.EPISODE_PREFIX.value: "111",
        "episode_part": "c",
        Metadata.VIDEO_TERM.value: "1080p",
        Metadata.FILE_NAME.value: "[horriblesubs] gintama - 111c [1080p]"
    },
    {
        Metadata.RELEASE_GROUP.value: "horriblesubsanimesenshi",
        Metadata.SERIES_TITLE.value: "heroman",
        Metadata.EPISODE_PREFIX.value: "10",
        Metadata.VIDEO_TERM.value: "xvid",
        Metadata.FILE_NAME.value: "[horriblesubs] heroman - 10_(xvid_animesenshi)"
    },
    {
        Metadata.RELEASE_GROUP.value: "horriblesubs",
        Metadata.SERIES_TITLE.value: "mob psycho 100",
        Metadata.SEASON_PREFIX.value: "s",
        Metadata.SEASON_PREFIX.value: "2",
        Metadata.EPISODE_PREFIX.value: "07",
        Metadata.VIDEO_TERM.value: "1080p",
        Metadata.FILE_NAME.value: "[horriblesubs] mob psycho 100 s2 - 07 [1080p]"
    },
    {
        Metadata.RELEASE_GROUP.value: "horriblesubs",
        Metadata.SERIES_TITLE.value: "momokuri",
        Metadata.EPISODE_PREFIX.value: [
            "01",
            "02"
        ],
        "range_separator": "+",
        Metadata.VIDEO_TERM.value: "720p",
        Metadata.FILE_NAME.value: "[horriblesubs] momokuri - 01+02 [720p]"
    },
    {
        Metadata.RELEASE_GROUP.value: "horriblesubs",
        Metadata.SERIES_TITLE.value: "the world god only knows 2",
        Metadata.EPISODE_PREFIX.value: "03",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.FILE_NAME.value: "[horriblesubs] the world god only knows 2 - 03 [720p]"
    },
    {
        Metadata.RELEASE_GROUP.value: "horriblesubs",
        Metadata.SERIES_TITLE.value: "tower of druaga - sword of uruk",
        Metadata.EPISODE_PREFIX.value: "04",
        Metadata.VIDEO_TERM.value: "480p",
        Metadata.FILE_NAME.value: "[horriblesubs] tower of druaga - sword of uruk - 04 [480p]"
    },
    {
        Metadata.RELEASE_GROUP.value: "horriblesubs",
        Metadata.SERIES_TITLE.value: "tsukimonogatari",
        Metadata.EPISODE_PREFIX.value: [
            "01",
            "04"
        ],
        "range_separator": "-",
        Metadata.VIDEO_TERM.value: "1080p",
        Metadata.FILE_NAME.value: "[horriblesubs] tsukimonogatari - (01-04) [1080p]"
    },
    {
        Metadata.RELEASE_GROUP.value: "infantjedi",
        Metadata.SERIES_TITLE.value: "norn9 - norn + nonetto",
        Metadata.EPISODE_PREFIX.value: "12",
        Metadata.FILE_NAME.value: "[infantjedi] norn9 - norn + nonetto - 12"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "aharen-san wa hakarenai",
        Metadata.SEASON_PREFIX.value: "s",
        Metadata.SEASON_PREFIX.value: "01",
        Metadata.EPISODE_PREFIX.value: "e",
        Metadata.EPISODE_PREFIX.value: "06",
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.FILE_NAME.value: "[judas] aharen-san wa hakarenai - s01e06v2"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "aharen-san wa hakarenai",
        Metadata.SEASON_PREFIX.value: "s",
        Metadata.SEASON_PREFIX.value: "01",
        Metadata.EPISODE_PREFIX.value: "e",
        Metadata.EPISODE_PREFIX.value: "06",
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.FILE_NAME.value: "[judas] aharen-san wa hakarenai - s01e06v2"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "black clover - jump special anime festa 2018",
        Metadata.FILE_NAME.value: "[judas] black clover - jump special anime festa 2018"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "boruto",
        Metadata.SERIES_TYPE.value: "ova",
        Metadata.EPISODE_PREFIX.value: "the day naruto became hokage",
        Metadata.FILE_NAME.value: "[judas] boruto - ova - the day naruto became hokage"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "card captor sakura - the movie",
        Metadata.EPISODE_PREFIX.value: "2",
        Metadata.EPISODE_PREFIX.value: "the sealed card",
        Metadata.FILE_NAME.value: "[judas] card captor sakura - the movie 2 - the sealed card"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "code geass",
        Metadata.SERIES_TYPE.value: "movie",
        Metadata.EPISODE_PREFIX.value: "02",
        Metadata.FILE_NAME.value: "[judas] code geass movie 02"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "code geass",
        Metadata.SERIES_TYPE.value: "movie",
        Metadata.EPISODE_PREFIX.value: "02",
        Metadata.EPISODE_PREFIX.value: "lelouch of the rebellion - transgression",
        Metadata.FILE_NAME.value: "[judas] code geass movie 02 - lelouch of the rebellion - transgression"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "gintama",
        Metadata.SEASON_PREFIX.value: "s",
        Metadata.SEASON_PREFIX.value: "01",
        Metadata.EPISODE_PREFIX.value: [
            "e",
            "e"
        ],
        Metadata.EPISODE_PREFIX.value: [
            "01",
            "02"
        ],
        "range_separator": [
            "-",
            "-"
        ],
        "episode_number_alt": [
            "001",
            "002"
        ],
        Metadata.FILE_NAME.value: "[judas] gintama - s01e01-e02 (001-002)"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "gintama",
        Metadata.SEASON_PREFIX.value: "s",
        Metadata.SEASON_PREFIX.value: "02",
        Metadata.EPISODE_PREFIX.value: [
            "e",
            "e"
        ],
        Metadata.EPISODE_PREFIX.value: [
            "01",
            "02"
        ],
        "range_separator": [
            "-",
            "-"
        ],
        "episode_number_alt": [
            "025",
            "026"
        ],
        Metadata.FILE_NAME.value: "[judas] gintama - s02e01-e02 (025-026)"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "grisaia no kajitsu",
        Metadata.SEASON_PREFIX.value: "s",
        Metadata.SEASON_PREFIX.value: "01",
        Metadata.SERIES_TYPE.value: "s",
        Metadata.EPISODE_PREFIX.value: "02",
        Metadata.FILE_NAME.value: "[judas] grisaia no kajitsu - s01s02"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "initial d - extra stage ",
        Metadata.EPISODE_PREFIX.value: "02",
        Metadata.EPISODE_PREFIX.value: "sentimental white",
        Metadata.FILE_NAME.value: "[judas] initial d - extra stage 02 - sentimental white"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "initial d - extra stage 2",
        Metadata.EPISODE_PREFIX.value: "sentimental white",
        Metadata.FILE_NAME.value: "[judas] initial d - extra stage 2 - sentimental white"
    },

    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "one piece",
        Metadata.EPISODE_PREFIX.value: "1009",
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.FILE_NAME.value: "[judas] one piece - 1009v2"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "one punch man",
        Metadata.SEASON_PREFIX.value: "s",
        Metadata.SEASON_PREFIX.value: "01",
        Metadata.SERIES_TYPE.value: "ova",
        Metadata.EPISODE_PREFIX.value: "02",
        Metadata.FILE_NAME.value: "[judas] one punch man - s01ova02"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "one-punch man",
        Metadata.SEASON_PREFIX.value: "season",
        Metadata.SEASON_PREFIX.value: "1",
        Metadata.SERIES_TYPE.value: "ova",
        Metadata.EPISODE_PREFIX.value: "05",
        Metadata.FILE_NAME.value: "[judas] one-punch man season 1 ova - 05"
    },
    {
        Metadata.RELEASE_GROUP.value: "jumonji-girishinsen-subsasf",
        Metadata.SERIES_TITLE.value: "d.c.ii da capo ii",
        Metadata.EPISODE_PREFIX.value: "ep",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.FILE_CHECKSUM.value: "a1fc58a7",
        Metadata.FILE_NAME.value: "[jumonji-giri]_[shinsen-subs][asf]_d.c.ii_da_capo_ii_ep01_(a1fc58a7)"
    },
    {
        Metadata.RELEASE_GROUP.value: "kaf-team",
        Metadata.SERIES_TITLE.value: "one piece",
        Metadata.SERIES_TYPE.value: "movie",
        Metadata.EPISODE_PREFIX.value: "9",
        Metadata.LANGUAGE.value: "vostfr",
        Metadata.VIDEO_TERM.value: "hd",
        Metadata.FILE_NAME.value: "[kaf-team]_one_piece_movie_9_vostfr_hd"
    },
    {
        Metadata.RELEASE_GROUP.value: "klf",
        Metadata.SERIES_TITLE.value: "d.gray-man",
        Metadata.EPISODE_PREFIX.value: "04",
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.FILE_NAME.value: "[klf]_d.gray-man_04v2"
    },
    {
        Metadata.RELEASE_GROUP.value: "kira-fansub",
        Metadata.SERIES_TITLE.value: "uchuu no stellvia",
        Metadata.EPISODE_PREFIX.value: "ep",
        Metadata.EPISODE_PREFIX.value: "14",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_TERM.value: [
            "h264",
            "24fps"
        ],
        Metadata.VIDEO_RESOLUTION.value: "1280x960",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "06ee7355",
        Metadata.FILE_NAME.value: "[kira-fansub] uchuu no stellvia ep 14 (bd h264 1280x960 24fps aac) [06ee7355]"
    },
    {
        Metadata.RELEASE_GROUP.value: "lrl",
        Metadata.SERIES_TITLE.value: "1001 nights",
        Metadata.SERIES_YEAR.value: "1998",
        Metadata.SOURCE.value: "dvd",
        Metadata.FILE_NAME.value: "[lrl] 1001 nights (1998) [dvd]"
    },
    {
        Metadata.RELEASE_GROUP.value: "lambda-delta",
        Metadata.SERIES_TITLE.value: "umineko no naku koro ni",
        Metadata.EPISODE_PREFIX.value: "11",
        Metadata.VIDEO_RESOLUTION.value: "848x480",
        Metadata.VIDEO_TERM.value: "h.264",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "943106ad",
        Metadata.FILE_NAME.value: "[lambda-delta]_umineko_no_naku_koro_ni_-_11_[848x480_h.264_aac][943106ad]"
    },
    {
        Metadata.RELEASE_GROUP.value: "mezashite",
        Metadata.SERIES_TITLE.value: "aikatsu!",
        Metadata.EPISODE_PREFIX.value: "100",
        Metadata.FILE_CHECKSUM.value: "d035a39f",
        Metadata.FILE_NAME.value: "[mezashite] aikatsu! \u2012 100 [d035a39f]"
    },
    {
        Metadata.RELEASE_GROUP.value: "n logn fansubs",
        Metadata.SERIES_TITLE.value: "angel beats",
        Metadata.EPISODE_PREFIX.value: "9",
        Metadata.FILE_NAME.value: "[n logn fansubs] angel beats (9)"
    },
    {
        Metadata.RELEASE_GROUP.value: "namaenai",
        Metadata.SERIES_TITLE.value: "hidamari sketch x365",
        Metadata.EPISODE_PREFIX.value: "09",
        "episode_part": "a",
        Metadata.SOURCE.value: "dvd",
        Metadata.FILE_CHECKSUM.value: "49874745",
        Metadata.FILE_NAME.value: "[namaenai] hidamari sketch x365 - 09a (dvd) [49874745]"
    },
    {
        Metadata.RELEASE_GROUP.value: "ninjapanda",
        Metadata.SERIES_TITLE.value: "tiger & bunny ",
        Metadata.EPISODE_PREFIX.value: "#",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.EPISODE_PREFIX.value: "all's well that ends well.",
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "3",
        Metadata.VIDEO_TERM.value: [
            "1080p",
            "hi10p"
        ],
        Metadata.AUDIO_TERM.value: [
            "da",
            "aac"
        ],
        Metadata.FILE_CHECKSUM.value: "4a9ab85f",
        Metadata.FILE_NAME.value: "[ninjapanda] tiger & bunny #01 all's well that ends well. (v3, 1080p hi10p, da aac) [4a9ab85f]"
    },
    {
        Metadata.RELEASE_GROUP.value: "nishi-taku",
        Metadata.SERIES_TITLE.value: "tamayura ~graduation photo~  part 1",
        Metadata.SERIES_TYPE.value: "movie",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.FILE_CHECKSUM.value: "98965607",
        Metadata.FILE_NAME.value: "[nishi-taku] tamayura ~graduation photo~ movie part 1 [bd][720p][98965607]"
    },
    {
        Metadata.RELEASE_GROUP.value: "nubles",
        Metadata.SERIES_TITLE.value: "space battleship yamato 2199",
        Metadata.SERIES_YEAR.value: "2012",
        Metadata.EPISODE_PREFIX.value: "episode",
        Metadata.EPISODE_PREFIX.value: "18",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.VIDEO_TERM.value: "8 bit",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "ba70ba9c",
        Metadata.FILE_NAME.value: "[nubles] space battleship yamato 2199 (2012) episode 18 (720p 8 bit aac)[ba70ba9c]"
    },
    {
        Metadata.RELEASE_GROUP.value: "r-r",
        Metadata.SERIES_TITLE.value: "diebuster",
        Metadata.EPISODE_PREFIX.value: "ep",
        Metadata.EPISODE_PREFIX.value: "1",
        Metadata.VIDEO_TERM.value: [
            "720p",
            "hi10p"
        ],
        Metadata.AUDIO_TERM.value: "ac3",
        Metadata.FILE_CHECKSUM.value: "82e36a36",
        Metadata.FILE_NAME.value: "[r-r] diebuster.ep1 (720p.hi10p.ac3) [82e36a36]"
    },
    {
        Metadata.RELEASE_GROUP.value: "rna",
        Metadata.SERIES_TITLE.value: "sakura taisen new york ny",
        Metadata.EPISODE_PREFIX.value: "ep",
        Metadata.EPISODE_PREFIX.value: "2",
        Metadata.FILE_CHECKSUM.value: "1590d378",
        Metadata.FILE_NAME.value: "[rna]_sakura_taisen_new_york_ny_ep_2_[1590d378]"
    },
    {
        Metadata.RELEASE_GROUP.value: "rax",
        Metadata.SERIES_TITLE.value: "mezzo(dsa)",
        Metadata.EPISODE_PREFIX.value: "05",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.AUDIO_TERM.value: "ogg",
        Metadata.FILE_CHECKSUM.value: "585d9971",
        Metadata.FILE_NAME.value: "[rax]mezzo(dsa)_-_05_-_[x264_ogg]_[585d9971]"
    },
    {
        Metadata.RELEASE_GROUP.value: "raizel",
        Metadata.SERIES_TITLE.value: "persona 4 the animation",
        Metadata.EPISODE_PREFIX.value: "episode",
        Metadata.EPISODE_PREFIX.value: "13",
        Metadata.EPISODE_PREFIX.value: "a stormy summer vacation part 1",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.AUDIO_TERM.value: [
            "dual",
            "audio",
            "flac"
        ],
        Metadata.VIDEO_TERM.value: "hi10p",
        Metadata.FILE_CHECKSUM.value: "8a45634b",
        Metadata.FILE_NAME.value: "[raizel] persona 4 the animation episode 13 - a stormy summer vacation part 1  [bd_1080p_dual_audio_flac_hi10p][8a45634b]"
    },
    {
        Metadata.RELEASE_GROUP.value: "rakuda",
        Metadata.SERIES_TITLE.value: "gift.~eternal.rainbow~",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.SOURCE.value: "dvd",
        Metadata.VIDEO_TERM.value: "h.264",
        Metadata.AUDIO_TERM.value: "vorbis",
        Metadata.FILE_NAME.value: "[rakuda].gift.~eternal.rainbow~.01.dvd.h.264.vorbis"
    },
    {
        Metadata.RELEASE_GROUP.value: "redone",
        Metadata.SERIES_TITLE.value: "memories off 3.5",
        Metadata.EPISODE_PREFIX.value: "04",
        Metadata.SOURCE.value: "dvd",
        Metadata.VIDEO_TERM.value: "10-bit",
        Metadata.FILE_NAME.value: "[redone] memories off 3.5 - 04 (dvd 10-bit)"
    },
    {
        Metadata.RELEASE_GROUP.value: "reaktor",
        Metadata.SERIES_TITLE.value: "serial experiments lain",
        Metadata.EPISODE_PREFIX.value: "e",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.VIDEO_TERM.value: [
            "x265",
            "10-bit"
        ],
        Metadata.AUDIO_TERM.value: "dual-audio",
        Metadata.FILE_NAME.value: "[reaktor] serial experiments lain - e01 [1080p][x265][10-bit][dual-audio]"
    },
    {
        Metadata.RELEASE_GROUP.value: "ruri",
        Metadata.SERIES_TITLE.value: "no.6",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.FILE_CHECKSUM.value: "a956075c",
        Metadata.FILE_NAME.value: "[ruri]no.6 01 [720p][h264][a956075c]"
    },
    {
        Metadata.RELEASE_GROUP.value: "sfw",
        Metadata.SERIES_TITLE.value: "queen's blade",
        Metadata.SEASON_PREFIX.value: "s",
        Metadata.SEASON_PREFIX.value: "2",
        Metadata.FILE_NAME.value: "[sfw]_queen's_blade_s2"
    },
    {
        Metadata.RELEASE_GROUP.value: "ss",
        Metadata.SERIES_TITLE.value: "kemono no souja erin",
        Metadata.EPISODE_PREFIX.value: "12",
        Metadata.VIDEO_RESOLUTION.value: "1280x720",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.FILE_CHECKSUM.value: "0f5f884f",
        Metadata.FILE_NAME.value: "[ss]_kemono_no_souja_erin_-_12_(1280x720_h264)_[0f5f884f]"
    },
    {
        Metadata.RELEASE_GROUP.value: "seto_otaku",
        Metadata.SERIES_TITLE.value: "aika zero",
        Metadata.SERIES_TYPE.value: "ova",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: "1920x1080",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.AUDIO_TERM.value: "flac",
        Metadata.FILE_CHECKSUM.value: "6730d40a",
        Metadata.FILE_NAME.value: "[seto_otaku]_aika_zero_ova_-_01_[bd][1920x1080_h264-flac][6730d40a]"
    },
    {
        Metadata.RELEASE_GROUP.value: "shinsen-subs",
        Metadata.SERIES_TITLE.value: "macross frontier",
        Metadata.EPISODE_PREFIX.value: "01",
        "episode_part": "b",
        Metadata.FILE_CHECKSUM.value: "4d5ec315",
        Metadata.FILE_NAME.value: "[shinsen-subs]_macross_frontier_-_01b_[4d5ec315]"
    },
    {
        Metadata.RELEASE_GROUP.value: "spoonsubs",
        Metadata.SERIES_TITLE.value: "hidamari sketch x365",
        Metadata.EPISODE_PREFIX.value: "04.1",
        Metadata.VIDEO_TERM.value: "dvd",
        Metadata.FILE_CHECKSUM.value: "b6ce8458",
        Metadata.FILE_NAME.value: "[spoonsubs]_hidamari_sketch_x365_-_04.1_(dvd)[b6ce8458]"
    },
    {
        Metadata.RELEASE_GROUP.value: "subdesu-h",
        "extra_info": [
            " ",
            " ",
            "version",
            " "
        ],
        Metadata.SERIES_TITLE.value: "swing out sisters",
        Metadata.RELEASE_INFORMATION.value: "complete",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.VIDEO_TERM.value: [
            "x264",
            "8bit"
        ],
        Metadata.AUDIO_TERM.value: "ac3",
        Metadata.FILE_CHECKSUM.value: "3abd57e6",
        Metadata.FILE_NAME.value: "[subdesu-h] swing out sisters complete version (720p x264 8bit ac3) [3abd57e6]"
    },
    {
        Metadata.RELEASE_GROUP.value: "tv-j",
        Metadata.SERIES_TITLE.value: "kidou senshi gundam uc unicorn",
        Metadata.EPISODE_PREFIX.value: "episode",
        Metadata.EPISODE_PREFIX.value: "02",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: "1920x1080",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.AUDIO_TERM.value: [
            "aac",
            "5.1ch"
        ],
        Metadata.LANGUAGE.value: [
            "jp",
            "en",
            "jp",
            "en",
            "sp",
            "fr",
            "ch"
        ],
        Metadata.SUBS_TERM.value: "sub",
        "other": "chap",
        Metadata.FILE_NAME.value: "[tv-j] kidou senshi gundam uc unicorn - episode.02 [bd 1920x1080 h264+aac(5.1ch jp+en) +sub(jp-en-sp-fr-ch) chap]"
    },
    {
        Metadata.RELEASE_GROUP.value: "taigasubs",
        Metadata.SERIES_TITLE.value: "toradora!",
        Metadata.SERIES_YEAR.value: "2008",
        Metadata.EPISODE_PREFIX.value: "01",
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.EPISODE_PREFIX.value: "tiger and dragon",
        Metadata.VIDEO_RESOLUTION.value: "1280x720",
        Metadata.VIDEO_TERM.value: "h.264",
        Metadata.AUDIO_TERM.value: "flac",
        Metadata.FILE_CHECKSUM.value: "1234abcd",
        Metadata.FILE_NAME.value: "[taigasubs]_toradora!_(2008)_-_01v2_-_tiger_and_dragon_[1280x720_h.264_flac][1234abcd]"
    },
    {
        Metadata.RELEASE_GROUP.value: "taka",
        Metadata.SERIES_TITLE.value: "fullmetal alchemist",
        Metadata.SERIES_YEAR.value: "2009",
        Metadata.EPISODE_PREFIX.value: "04",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.FILE_CHECKSUM.value: "40f2a957",
        Metadata.FILE_NAME.value: "[taka]_fullmetal_alchemist_(2009)_04_[720p][40f2a957]"
    },
    {
        Metadata.RELEASE_GROUP.value: "triad",
        Metadata.SERIES_TITLE.value: "today in class 5-2",
        Metadata.EPISODE_PREFIX.value: "04",
        Metadata.FILE_NAME.value: "[triad]_today_in_class_5-2_-_04"
    },
    {
        Metadata.RELEASE_GROUP.value: "tsundere",
        Metadata.SERIES_TITLE.value: "hyouka",
        Metadata.EPISODE_PREFIX.value: [
            "01",
            "04"
        ],
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "2",
        "range_separator": "-",
        Metadata.SOURCE.value: "bdrip",
        Metadata.VIDEO_TERM.value: [
            "h264",
            "10bit"
        ],
        Metadata.VIDEO_RESOLUTION.value: "1920x1080",
        Metadata.AUDIO_TERM.value: "flac",
        Metadata.FILE_NAME.value: "[tsundere] hyouka - 01v2-04 [bdrip h264 1920x1080 10bit flac]"
    },
    {
        Metadata.RELEASE_GROUP.value: "utw-thora",
        Metadata.SERIES_TITLE.value: "evangelion 3.33 you can (not) redo",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.AUDIO_TERM.value: "flac",
        Metadata.FILE_CHECKSUM.value: "f2060cf5",
        Metadata.FILE_NAME.value: "[utw-thora] evangelion 3.33 you can (not) redo [bd][1080p,x264,flac][f2060cf5]"
    },
    {
        Metadata.RELEASE_GROUP.value: "utw-tmd",
        Metadata.SERIES_TITLE.value: "summer wars",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.AUDIO_TERM.value: "truehd5.1",
        Metadata.FILE_CHECKSUM.value: "9f311dab",
        Metadata.FILE_NAME.value: "[utw-tmd]_summer_wars_[bd][h264-720p][truehd5.1][9f311dab]"
    },
    {
        Metadata.RELEASE_GROUP.value: "utw",
        Metadata.SERIES_TITLE.value: "accel world - ex01",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "3e56ee18",
        Metadata.FILE_NAME.value: "[utw]_accel_world_-_ex01_[bd][h264-720p_aac][3e56ee18]"
    },
    {
        Metadata.RELEASE_GROUP.value: "utw",
        Metadata.SERIES_TITLE.value: "fate zero",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "720"
        },
        Metadata.AUDIO_TERM.value: "ac3",
        Metadata.FILE_CHECKSUM.value: "02a0491d",
        Metadata.FILE_NAME.value: "[utw]_fate_zero_-_01_[bd][h264-720p_ac3][02a0491d]"
    },
    {
        Metadata.RELEASE_GROUP.value: "urusai",
        Metadata.SERIES_TITLE.value: "bokura ga ita",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.SOURCE.value: "dvd",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.AUDIO_TERM.value: "ac3",
        Metadata.FILE_CHECKSUM.value: "bfce1627",
        Metadata.RELEASE_INFORMATION.value: "fixed",
        Metadata.FILE_NAME.value: "[urusai]_bokura_ga_ita_01_[dvd_h264_ac3]_[bfce1627][fixed]"
    },
    {
        Metadata.RELEASE_GROUP.value: "valdikss",
        Metadata.SERIES_TITLE.value: "first squad the morment of truth",
        Metadata.VIDEO_RESOLUTION.value: "720x576",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.SOURCE.value: "dvdscr",
        Metadata.LANGUAGE.value: "eng",
        "subtitle_type": "hardsub",
        Metadata.FILE_NAME.value: "[valdikss]_first_squad_the_morment_of_truth_[720x576_h264_dvdscr_eng_hardsub]"
    },
    {
        Metadata.RELEASE_GROUP.value: "yoroshiku",
        Metadata.SERIES_TITLE.value: "009-1",
        Metadata.EPISODE_PREFIX.value: "02",
        Metadata.VIDEO_TERM.value: "h264",
        Metadata.FILE_CHECKSUM.value: "36d2444d",
        Metadata.FILE_NAME.value: "[yoroshiku]_009-1_-_02_(h264)_[36d2444d]"
    },
    {
        Metadata.RELEASE_GROUP.value: "yuurisan-subs",
        Metadata.SERIES_TITLE.value: "darker than black - gemini of the meteor",
        Metadata.EPISODE_PREFIX.value: "01",
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.FILE_CHECKSUM.value: "65274fde",
        Metadata.RELEASE_INFORMATION.value: "patch",
        Metadata.FILE_NAME.value: "[yuurisan-subs]_darker_than_black_-_gemini_of_the_meteor_-_01v2_[65274fde].patch"
    },
    {
        Metadata.RELEASE_GROUP.value: "zero-raws",
        Metadata.SERIES_TITLE.value: "shingeki no kyojin",
        Metadata.EPISODE_PREFIX.value: "25",
        Metadata.RELEASE_INFORMATION.value: "end",
        Metadata.SOURCE.value: "mbs",
        Metadata.VIDEO_RESOLUTION.value: "1280x720",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_NAME.value: "[zero-raws] shingeki no kyojin - 25 end (mbs 1280x720 x264 aac)"
    },
    {
        Metadata.RELEASE_GROUP.value: "zom-b",
        Metadata.SERIES_TITLE.value: "machine-doll wa kizutsukanai",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.EPISODE_PREFIX.value: "facing ''cannibal candy'' i ",
        "other": [
            "kuroi",
            "fff"
        ],
        Metadata.RELEASE_INFORMATION.value: "remux",
        Metadata.FILE_CHECKSUM.value: "b99c8ded",
        Metadata.FILE_NAME.value: "[zom-b] machine-doll wa kizutsukanai - 01 - facing ''cannibal candy'' i (kuroi, fff remux) [b99c8ded]"
    },
    {
        Metadata.RELEASE_GROUP.value: "zurako",
        Metadata.SERIES_TITLE.value: "sora no woto",
        Metadata.EPISODE_PREFIX.value: "07.5",
        Metadata.EPISODE_PREFIX.value: "drinking party - fortress battle",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "f7df16f7",
        Metadata.FILE_NAME.value: "[zurako] sora no woto - 07.5 - drinking party - fortress battle (bd 1080p aac) [f7df16f7]"
    },
    {
        Metadata.RELEASE_GROUP.value: "zza",
        Metadata.SERIES_TITLE.value: "nanatsu no taizai - s03 - kamigami no gekirin",
        Metadata.EPISODE_PREFIX.value: "21",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.VIDEO_TERM.value: "x265",
        Metadata.FILE_NAME.value: "[zza] nanatsu no taizai - s03 - kamigami no gekirin - 21 [1080p.x265]"
    },
    {
        Metadata.RELEASE_GROUP.value: "a4e",
        Metadata.SERIES_TITLE.value: "r.o.d the tv",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.VIDEO_TERM.value: "divx",
        "extra_info": "5.2.1",
        Metadata.FILE_NAME.value: "[a4e]r.o.d_the_tv_01[divx5.2.1]"
    },
    {
        Metadata.RELEASE_GROUP.value: "chibi-doki",
        Metadata.SERIES_TITLE.value: "seikon no qwaser",
        Metadata.EPISODE_PREFIX.value: "13",
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "0",
        Metadata.RELEASE_INFORMATION.value: [
            "uncensored",
            "director's",
            " ",
            "cut"
        ],
        Metadata.FILE_CHECKSUM.value: "988db090",
        Metadata.FILE_NAME.value: "[chibi-doki] seikon no qwaser - 13v0 (uncensored director's cut) [988db090]"
    },
    {
        Metadata.RELEASE_GROUP.value: "fong",
        Metadata.SERIES_TITLE.value: "lupin iii - kutabare! nostradamus",
        Metadata.SOURCE.value: "bdrip",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.VIDEO_TERM.value: "10bit",
        Metadata.AUDIO_TERM.value: "multiaudio",
        Metadata.FILE_NAME.value: "[fong] lupin iii - kutabare! nostradamus [bdrip.1080p.10bit.multiaudio]"
    },
    {
        Metadata.RELEASE_GROUP.value: "gg",
        Metadata.SERIES_TITLE.value: "kimi ni todoke",
        Metadata.SEASON_PREFIX.value: "2nd",
        Metadata.SEASON_PREFIX.value: "season",
        Metadata.EPISODE_PREFIX.value: "00",
        Metadata.FILE_CHECKSUM.value: "bf735bc4",
        Metadata.FILE_NAME.value: "[gg]_kimi_ni_todoke_2nd_season_-_00_[bf735bc4]"
    },
    {
        Metadata.RELEASE_GROUP.value: "kito",
        Metadata.SERIES_TITLE.value: "nazca",
        Metadata.EPISODE_PREFIX.value: "episode",
        Metadata.EPISODE_PREFIX.value: "01",
        Metadata.SOURCE.value: "dvdrip",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.AUDIO_TERM.value: "he-aac",
        Metadata.LANGUAGE.value: [
            "jpn",
            "fr"
        ],
        Metadata.SUBS_TERM.value: "sub",
        Metadata.FILE_NAME.value: "[kito].nazca.episode.01.dvdrip.[x264.he-aac.{jpn}+sub{fr}]"
    },
    {
        Metadata.RELEASE_GROUP.value: "tlacatlc6",
        Metadata.SERIES_TITLE.value: "natsume yuujinchou shi",
        Metadata.VOLUME_PREFIX.value: [
            "vol.",
            "vol."
        ],
        "volume_number": [
            "1",
            "2"
        ],
        "release_prefix": "v",
        Metadata.RELEASE_VERSION.value: "2",
        "range_separator": "&",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: "1280x720",
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_NAME.value: "[tlacatlc6] natsume yuujinchou shi vol. 1v2 & vol. 2 (bd 1280x720 x264 aac)"
    },
    {
        Metadata.RELEASE_GROUP.value: "akihitosubs",
        Metadata.SERIES_TITLE.value: "elfen lied",
        Metadata.EPISODE_PREFIX.value: "12",
        Metadata.SOURCE.value: "bd",
        Metadata.VIDEO_RESOLUTION.value: "1920x1080",
        Metadata.VIDEO_TERM.value: [
            "x265",
            "10bit"
        ],
        Metadata.AUDIO_TERM.value: [
            "5.1",
            "aac"
        ],
        Metadata.FILE_NAME.value: "]akihitosubs] elfen lied - 12 [bd 1920x1080 x265 10bit 5.1 aac]"
    },
    {
        Metadata.SERIES_TITLE.value: "Byousoku 5 Centimeter",
        Metadata.SOURCE.value: "Blu-ray",
        Metadata.VIDEO_RESOLUTION.value: "1920x1080",
        Metadata.VIDEO_TERM.value: "h.264",
        Metadata.AUDIO_TERM.value: [
            "2.0ch",
            "AAC"
        ],
        "subtitle_type": "softsubs",
        Metadata.FILE_NAME.value: "Byousoku 5 Centimeter [Blu-ray][1920x1080 h.264][2.0ch AAC][softsubs]"
    },
    {
        Metadata.SERIES_TITLE.value: "FAIRY TAIL",
        Metadata.SERIES_YEAR.value: "2014",
        Metadata.FILE_NAME.value: "FAIRY TAIL (2014)"
    },
    {
        Metadata.SERIES_TITLE.value: "Little Witch Academia",
        Metadata.SERIES_TYPE.value: "TV",
        Metadata.FILE_NAME.value: "Little Witch Academia (TV)"
    },
    {
        Metadata.SERIES_TITLE.value: "Arslan Senki (TV)",
        Metadata.SERIES_TYPE.value: "OVA",
        Metadata.FILE_NAME.value: "Arslan Senki (TV) OVA"
    },
    {
        Metadata.SERIES_TITLE.value: "Example Anime",
        Metadata.SERIES_TYPE.value: "TV",
        Metadata.SERIES_YEAR.value: "2020",
        Metadata.FILE_NAME.value: "Example Anime (TV) (2020)"
    },
    {
        Metadata.RELEASE_GROUP.value: "Judas",
        Metadata.SERIES_TITLE.value: "Kimetsu no Yaiba",
        Metadata.SERIES_TYPE.value: "NCED",
        "episode_number_special": "02",
        Metadata.EPISODE_PREFIX.value: "ep",
        Metadata.EPISODE_PREFIX.value: "19",
        Metadata.FILE_NAME.value: "[Judas] Kimetsu no Yaiba - NCED02 (ep 19)"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "heavy object",
        Metadata.SERIES_TYPE.value: "nced",
        "episode_number_special": "01",
        Metadata.FILE_NAME.value: "[judas] heavy object - nced 01"
    },
    {
        Metadata.SERIES_TITLE.value: "The Eminence in Shadow",
        Metadata.VOLUME_PREFIX.value: "vol",
        "volume_number": "2",
        Metadata.EPISODE_PREFIX.value: "06",
        Metadata.EPISODE_PREFIX.value: "Pretenders",
        Metadata.FILE_NAME.value: "The Eminence in Shadow vol 2 06 Pretenders"
    },
    {
        'anime_title': 'A Certain Scientific Railgun',
        'anime_season_prefix': 'S',
        'anime_season': 2,
        'file_name': 'A.Certain.Scientific.Railgun.S02.1080p-Hi10p.BluRay.FLAC2.0.x264-CTR (English Dubbed Dual Audio)',
        'video_resolution': '1080p',
        'video_term': 'Hi10p',
        'source': 'BluRay',
        'other': ['FLAC2.0', 'x264-CTR'],
        'language': 'English',
        'subtitles': 'Dubbed',
        'audio_term': 'Dual Audio'
    },
    {
        Metadata.SEASON_PREFIX.value: [1, 2, 3, 4],
        Metadata.SEASON_PREFIX.value: ["S", "S", "S", "S"],
        Metadata.SERIES_TITLE.value: "Sword Art Online",
        Metadata.AUDIO_TERM.value: ["Dual Audio", "AAC"],
        "batch": [1, 2, 3, 4, "Alternative", "Movies", "Specials", "OVAs"],
        Metadata.FILE_NAME.value: "[Anime Time] Sword Art Online (S01+S02+S03+S04+Alternative+Movies+Specials+OVAs) "
                                  "[BD] [Dual Audio][1080p][HEVC 10bit x265][AAC][Eng Sub] [Batch] (SAO)",
        Metadata.LANGUAGE.value: "Eng",
        "other": ["Alternative", "Movies", "Specials", "OVAs", "SAO"],
        Metadata.RELEASE_GROUP.value: "Anime Time",
        Metadata.RELEASE_INFORMATION.value: "Batch",
        Metadata.SOURCE.value: "BD",
        Metadata.SUBS_TERM.value: "Sub",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.VIDEO_TERM.value: ["HEVC", "10bit", "x265"]
    }
]

something = [
    {
        Metadata.RELEASE_GROUP.value: "Coalgirls",
        Metadata.SERIES_TITLE.value: "bakemonogatari",
        Metadata.SERIES_TYPE.value: "op",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "4",
            Metadata.SEQUENCE_PART.value: "a"
        },
        Metadata.VIDEO_RESOLUTION.value: "1280x720",
        Metadata.SOURCE.value: "blu-ray",
        Metadata.AUDIO_TERM.value: "flac",
        Metadata.FILE_CHECKSUM.value: "327a2375",
        Metadata.FILE_NAME.value: "[Coalgirls]_bakemonogatari_op4a_(1280x720_blu-ray_flac)_[327a2375]"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "black clover",
        Metadata.SERIES_TYPE.value: "ncop",
        "episode_number_special": "10",
        "episode_part": "b",
        Metadata.EPISODE_PREFIX.value: "black catcher",
        Metadata.FILE_NAME.value: "[judas] black clover - ncop 10b - black catcher"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "nogizaka haruka no himitsu",
        Metadata.SERIES_TYPE.value: [
            "ova",
            "ncop"
        ],
        Metadata.FILE_NAME.value: "[judas] nogizaka haruka no himitsu - ova ncop"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "amanchu!",
        Metadata.SEASON_PREFIX.value: "s",
        Metadata.SEASON_PREFIX.value: "1",
        Metadata.SERIES_TYPE.value: "ending",
        Metadata.FILE_NAME.value: "[judas] amanchu! s1 - ending"
    },
    {
        Metadata.RELEASE_GROUP.value: "judas",
        Metadata.SERIES_TITLE.value: "granblue fantasy",
        Metadata.SERIES_TYPE.value: [
            "clean",
            " ",
            "ending"
        ],
        Metadata.FILE_NAME.value: "[judas] granblue fantasy - clean ending"
    },
    {
        Metadata.RELEASE_GROUP.value: "AnimeRG",
        Metadata.SERIES_TITLE.value: "Witch Craft Works",
        Metadata.SERIES_TYPE.value: "ED",
        Metadata.RELEASE_VERSION.value: "2",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.VIDEO_TERM.value: "x265",
        Metadata.FILE_NAME.value: "[AnimeRG] Witch Craft Works - EDv2 [1080p] [x265] [pseudo]"
    },
    {
        Metadata.RELEASE_GROUP.value: "coalgirls",
        Metadata.SERIES_TITLE.value: "toradora",
        Metadata.SERIES_TYPE.value: "ed",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "2"
        },
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_WIDTH.value: "704",
            Metadata.VIDEO_HEIGHT.value: "480"
        },
        Metadata.SOURCE.value: "dvd",
        Metadata.AUDIO_TERM.value: "aac",
        Metadata.FILE_CHECKSUM.value: "3b65d1e6",
        Metadata.FILE_NAME.value: "[coalgirls]_toradora_ed2_(704x480_dvd_aac)_[3b65d1e6]"
    },
    {
        Metadata.RELEASE_GROUP.value: "asenshi",
        Metadata.SERIES_TITLE.value: "rozen maiden 3",
        Metadata.SERIES_TYPE.value: "PV",
        Metadata.FILE_CHECKSUM.value: "ca57f300",
        Metadata.FILE_NAME.value: "[asenshi] rozen maiden 3 - PV [ca57f300]"
    },
{
        Metadata.RELEASE_GROUP.value: "fff",
        Metadata.SERIES_TITLE.value: "love live! the school idol movie",
        Metadata.SERIES_TYPE.value: "pv",
        Metadata.FILE_CHECKSUM.value: "d1a15d2c",
        Metadata.FILE_NAME.value: "[fff] love live! the school idol movie - pv [d1a15d2c]"
    },
    {
        Metadata.RELEASE_GROUP.value: "ane",
        Metadata.SERIES_TITLE.value: "yosuga no sora",
        Metadata.EPISODE_PREFIX.value: {
            Metadata.SEQUENCE_NUMBER.value: "01"
        },
        Metadata.SERIES_TYPE.value: "preview",
        Metadata.RELEASE_VERSION.value: "yorihime",
        Metadata.SOURCE.value: "bdrip",
        Metadata.VIDEO_RESOLUTION.value: {
            Metadata.VIDEO_HEIGHT.value: "1080"
        },
        Metadata.VIDEO_TERM.value: "x264",
        Metadata.AUDIO_TERM.value: "flac",
        Metadata.FILE_NAME.value: "[ane] yosuga no sora - ep01 preview (yorihime ver) [bdrip 1080p x264 flac]"
    },
]
