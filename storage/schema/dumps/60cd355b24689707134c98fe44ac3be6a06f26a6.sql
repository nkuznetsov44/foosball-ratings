--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Homebrew)
-- Dumped by pg_dump version 14.5 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: city; Type: TYPE; Schema: public; Owner: ratings
--

CREATE TYPE public.city AS ENUM (
    'MOSCOW',
    'SAINT_PETERSBURG',
    'KALININGRAD',
    'NOVOSIBIRSK',
    'TOMSK',
    'EKATERINBURG',
    'YAROSLAVL',
    'TULA'
);


ALTER TYPE public.city OWNER TO ratings;

--
-- Name: competitiontype; Type: TYPE; Schema: public; Owner: ratings
--

CREATE TYPE public.competitiontype AS ENUM (
    'OS',
    'OD',
    'WS',
    'WD',
    'MS',
    'MD',
    'AS',
    'AD',
    'NS',
    'ND',
    'SPS',
    'SPD',
    'COD',
    'MIXED',
    'PROAM'
);


ALTER TYPE public.competitiontype OWNER TO ratings;

--
-- Name: evksplayerrank; Type: TYPE; Schema: public; Owner: ratings
--

CREATE TYPE public.evksplayerrank AS ENUM (
    'BEGINNER',
    'NOVICE',
    'AMATEUR',
    'SEMIPRO',
    'PRO',
    'MASTER'
);


ALTER TYPE public.evksplayerrank OWNER TO ratings;

--
-- Name: ratingsstatestatus; Type: TYPE; Schema: public; Owner: ratings
--

CREATE TYPE public.ratingsstatestatus AS ENUM (
    'PUBLISHED',
    'READY_TO_PUBLISH',
    'ROLLED_BACK'
);


ALTER TYPE public.ratingsstatestatus OWNER TO ratings;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: competitions; Type: TABLE; Schema: public; Owner: ratings
--

CREATE TABLE public.competitions (
    id integer NOT NULL,
    external_id integer,
    tournament_id integer,
    competition_type public.competitiontype,
    evks_importance_coefficient numeric,
    start_datetime timestamp with time zone,
    end_datetime timestamp with time zone
);


ALTER TABLE public.competitions OWNER TO ratings;

--
-- Name: competitions_id_seq; Type: SEQUENCE; Schema: public; Owner: ratings
--

CREATE SEQUENCE public.competitions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.competitions_id_seq OWNER TO ratings;

--
-- Name: competitions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ratings
--

ALTER SEQUENCE public.competitions_id_seq OWNED BY public.competitions.id;


--
-- Name: matches; Type: TABLE; Schema: public; Owner: ratings
--

CREATE TABLE public.matches (
    id integer NOT NULL,
    external_id integer,
    competition_id integer,
    first_team_id integer,
    second_team_id integer,
    start_datetime timestamp with time zone,
    end_datetime timestamp with time zone,
    force_qualification boolean
);


ALTER TABLE public.matches OWNER TO ratings;

--
-- Name: matches_id_seq; Type: SEQUENCE; Schema: public; Owner: ratings
--

CREATE SEQUENCE public.matches_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matches_id_seq OWNER TO ratings;

--
-- Name: matches_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ratings
--

ALTER SEQUENCE public.matches_id_seq OWNED BY public.matches.id;


--
-- Name: player_states; Type: TABLE; Schema: public; Owner: ratings
--

CREATE TABLE public.player_states (
    id integer NOT NULL,
    previous_state_id integer,
    player_id integer,
    matches_played integer,
    matches_won integer,
    last_match_id integer,
    ratings json,
    evks_rank public.evksplayerrank,
    is_evks_rating_active boolean
);


ALTER TABLE public.player_states OWNER TO ratings;

--
-- Name: player_states_id_seq; Type: SEQUENCE; Schema: public; Owner: ratings
--

CREATE SEQUENCE public.player_states_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.player_states_id_seq OWNER TO ratings;

--
-- Name: player_states_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ratings
--

ALTER SEQUENCE public.player_states_id_seq OWNED BY public.player_states.id;


--
-- Name: players; Type: TABLE; Schema: public; Owner: ratings
--

CREATE TABLE public.players (
    id integer NOT NULL,
    external_id integer,
    first_name character varying(255),
    last_name character varying(255),
    city public.city
);


ALTER TABLE public.players OWNER TO ratings;

--
-- Name: players_id_seq; Type: SEQUENCE; Schema: public; Owner: ratings
--

CREATE SEQUENCE public.players_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.players_id_seq OWNER TO ratings;

--
-- Name: players_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ratings
--

ALTER SEQUENCE public.players_id_seq OWNED BY public.players.id;


--
-- Name: ratings_state_player_states; Type: TABLE; Schema: public; Owner: ratings
--

CREATE TABLE public.ratings_state_player_states (
    player_state_id integer,
    ratings_state_id integer
);


ALTER TABLE public.ratings_state_player_states OWNER TO ratings;

--
-- Name: ratings_states; Type: TABLE; Schema: public; Owner: ratings
--

CREATE TABLE public.ratings_states (
    id integer NOT NULL,
    previous_state_id integer,
    last_competition_id integer,
    status public.ratingsstatestatus
);


ALTER TABLE public.ratings_states OWNER TO ratings;

--
-- Name: ratings_states_id_seq; Type: SEQUENCE; Schema: public; Owner: ratings
--

CREATE SEQUENCE public.ratings_states_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ratings_states_id_seq OWNER TO ratings;

--
-- Name: ratings_states_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ratings
--

ALTER SEQUENCE public.ratings_states_id_seq OWNED BY public.ratings_states.id;


--
-- Name: sets; Type: TABLE; Schema: public; Owner: ratings
--

CREATE TABLE public.sets (
    id integer NOT NULL,
    external_id integer,
    match_id integer,
    "order" integer,
    first_team_score integer,
    second_team_score integer
);


ALTER TABLE public.sets OWNER TO ratings;

--
-- Name: sets_id_seq; Type: SEQUENCE; Schema: public; Owner: ratings
--

CREATE SEQUENCE public.sets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sets_id_seq OWNER TO ratings;

--
-- Name: sets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ratings
--

ALTER SEQUENCE public.sets_id_seq OWNED BY public.sets.id;


--
-- Name: teams; Type: TABLE; Schema: public; Owner: ratings
--

CREATE TABLE public.teams (
    id integer NOT NULL,
    competition_id integer,
    external_id integer,
    competition_place integer,
    first_player_id integer,
    second_player_id integer
);


ALTER TABLE public.teams OWNER TO ratings;

--
-- Name: teams_id_seq; Type: SEQUENCE; Schema: public; Owner: ratings
--

CREATE SEQUENCE public.teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.teams_id_seq OWNER TO ratings;

--
-- Name: teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ratings
--

ALTER SEQUENCE public.teams_id_seq OWNED BY public.teams.id;


--
-- Name: tournaments; Type: TABLE; Schema: public; Owner: ratings
--

CREATE TABLE public.tournaments (
    id integer NOT NULL,
    external_id integer,
    name character varying(255),
    city public.city,
    url character varying(511)
);


ALTER TABLE public.tournaments OWNER TO ratings;

--
-- Name: tournaments_id_seq; Type: SEQUENCE; Schema: public; Owner: ratings
--

CREATE SEQUENCE public.tournaments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tournaments_id_seq OWNER TO ratings;

--
-- Name: tournaments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ratings
--

ALTER SEQUENCE public.tournaments_id_seq OWNED BY public.tournaments.id;


--
-- Name: competitions id; Type: DEFAULT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.competitions ALTER COLUMN id SET DEFAULT nextval('public.competitions_id_seq'::regclass);


--
-- Name: matches id; Type: DEFAULT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.matches ALTER COLUMN id SET DEFAULT nextval('public.matches_id_seq'::regclass);


--
-- Name: player_states id; Type: DEFAULT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.player_states ALTER COLUMN id SET DEFAULT nextval('public.player_states_id_seq'::regclass);


--
-- Name: players id; Type: DEFAULT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.players ALTER COLUMN id SET DEFAULT nextval('public.players_id_seq'::regclass);


--
-- Name: ratings_states id; Type: DEFAULT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.ratings_states ALTER COLUMN id SET DEFAULT nextval('public.ratings_states_id_seq'::regclass);


--
-- Name: sets id; Type: DEFAULT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.sets ALTER COLUMN id SET DEFAULT nextval('public.sets_id_seq'::regclass);


--
-- Name: teams id; Type: DEFAULT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.teams ALTER COLUMN id SET DEFAULT nextval('public.teams_id_seq'::regclass);


--
-- Name: tournaments id; Type: DEFAULT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.tournaments ALTER COLUMN id SET DEFAULT nextval('public.tournaments_id_seq'::regclass);


--
-- Name: competitions competitions_pkey; Type: CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.competitions
    ADD CONSTRAINT competitions_pkey PRIMARY KEY (id);


--
-- Name: competitions competitions_tournament_id_external_id_key; Type: CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.competitions
    ADD CONSTRAINT competitions_tournament_id_external_id_key UNIQUE (tournament_id, external_id);


--
-- Name: matches matches_competition_id_external_id_key; Type: CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.matches
    ADD CONSTRAINT matches_competition_id_external_id_key UNIQUE (competition_id, external_id);


--
-- Name: matches matches_pkey; Type: CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.matches
    ADD CONSTRAINT matches_pkey PRIMARY KEY (id);


--
-- Name: player_states player_states_pkey; Type: CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.player_states
    ADD CONSTRAINT player_states_pkey PRIMARY KEY (id);


--
-- Name: players players_pkey; Type: CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (id);


--
-- Name: ratings_states ratings_states_pkey; Type: CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.ratings_states
    ADD CONSTRAINT ratings_states_pkey PRIMARY KEY (id);


--
-- Name: sets sets_match_id_external_id_key; Type: CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.sets
    ADD CONSTRAINT sets_match_id_external_id_key UNIQUE (match_id, external_id);


--
-- Name: sets sets_pkey; Type: CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.sets
    ADD CONSTRAINT sets_pkey PRIMARY KEY (id);


--
-- Name: teams teams_competition_id_external_id_key; Type: CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_competition_id_external_id_key UNIQUE (competition_id, external_id);


--
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (id);


--
-- Name: tournaments tournaments_external_id_key; Type: CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.tournaments
    ADD CONSTRAINT tournaments_external_id_key UNIQUE (external_id);


--
-- Name: tournaments tournaments_pkey; Type: CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.tournaments
    ADD CONSTRAINT tournaments_pkey PRIMARY KEY (id);


--
-- Name: competitions competitions_tournament_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.competitions
    ADD CONSTRAINT competitions_tournament_id_fkey FOREIGN KEY (tournament_id) REFERENCES public.tournaments(id);


--
-- Name: matches matches_competition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.matches
    ADD CONSTRAINT matches_competition_id_fkey FOREIGN KEY (competition_id) REFERENCES public.competitions(id);


--
-- Name: matches matches_first_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.matches
    ADD CONSTRAINT matches_first_team_id_fkey FOREIGN KEY (first_team_id) REFERENCES public.teams(id);


--
-- Name: matches matches_second_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.matches
    ADD CONSTRAINT matches_second_team_id_fkey FOREIGN KEY (second_team_id) REFERENCES public.teams(id);


--
-- Name: player_states player_states_last_match_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.player_states
    ADD CONSTRAINT player_states_last_match_id_fkey FOREIGN KEY (last_match_id) REFERENCES public.matches(id);


--
-- Name: player_states player_states_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.player_states
    ADD CONSTRAINT player_states_player_id_fkey FOREIGN KEY (player_id) REFERENCES public.players(id);


--
-- Name: player_states player_states_previous_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.player_states
    ADD CONSTRAINT player_states_previous_state_id_fkey FOREIGN KEY (previous_state_id) REFERENCES public.player_states(id);


--
-- Name: ratings_state_player_states ratings_state_player_states_player_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.ratings_state_player_states
    ADD CONSTRAINT ratings_state_player_states_player_state_id_fkey FOREIGN KEY (player_state_id) REFERENCES public.player_states(id);


--
-- Name: ratings_state_player_states ratings_state_player_states_ratings_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.ratings_state_player_states
    ADD CONSTRAINT ratings_state_player_states_ratings_state_id_fkey FOREIGN KEY (ratings_state_id) REFERENCES public.ratings_states(id);


--
-- Name: ratings_states ratings_states_last_competition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.ratings_states
    ADD CONSTRAINT ratings_states_last_competition_id_fkey FOREIGN KEY (last_competition_id) REFERENCES public.competitions(id);


--
-- Name: ratings_states ratings_states_previous_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.ratings_states
    ADD CONSTRAINT ratings_states_previous_state_id_fkey FOREIGN KEY (previous_state_id) REFERENCES public.ratings_states(id);


--
-- Name: sets sets_match_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.sets
    ADD CONSTRAINT sets_match_id_fkey FOREIGN KEY (match_id) REFERENCES public.matches(id);


--
-- Name: teams teams_competition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_competition_id_fkey FOREIGN KEY (competition_id) REFERENCES public.competitions(id);


--
-- Name: teams teams_first_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_first_player_id_fkey FOREIGN KEY (first_player_id) REFERENCES public.players(id);


--
-- Name: teams teams_second_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ratings
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_second_player_id_fkey FOREIGN KEY (second_player_id) REFERENCES public.players(id);


--
-- PostgreSQL database dump complete
--

