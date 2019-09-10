USE [SMBIANCAV20]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE SCHEMA [comet]
GO

CREATE TABLE [comet].[organisations](
	[organisationFifaId] [int] NOT NULL,
	[organisationName] [varchar](100) NULL,
	[organisationNature] [varchar](100) NULL,
	[organisationShortName] [varchar](100) NULL,
	[lastUpdate] [datetime] NULL,
 CONSTRAINT [pk_organisations] PRIMARY KEY CLUSTERED ([organisationFifaId] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]) ON [PRIMARY]
GO

CREATE TABLE [comet].[competitions](
	[competitionFifaId] [int] NOT NULL,
	[organisationFifaId] [int] NULL,
	[superiorCompetitionFifaId] [int] NULL,
	[status] [varchar](100) NULL,
	[internationalName] [varchar](100) NULL,
	[internationalShortName] [varchar](100) NULL,
	[season] [int] NULL,
	[ageCategory] [varchar](100) NULL,
	[ageCategoryName] [varchar](100) NULL,
	[dateFrom] [date] NULL,
	[dateTo] [date] NULL,
	[discipline] [varchar](100) NULL,
	[gender] [varchar](100) NULL,
	[imageId] [int] NULL,
	[multiplier] [int] NULL,
	[nature] [varchar](100) NULL,
	[numberOfParticipants] [int] NULL,
	[orderNumber] [int] NULL,
	[teamCharacter] [varchar](100) NULL,
	[flyingSubstitutions] [bit] NULL,
	[penaltyShootout] [bit] NULL,
	[matchType] [varchar](100) NULL,
	[pictureContentType] [varchar](100) NULL,
	[pictureLink] [varchar](100) NULL,
	[pictureValue] [varchar](100) NULL,
	[lastUpdate] [datetime] NULL,
 CONSTRAINT [pk_competitions] PRIMARY KEY CLUSTERED([competitionFifaId] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]) ON [PRIMARY]
GO

ALTER TABLE [comet].[competitions] WITH CHECK ADD CONSTRAINT [fk_organisations_competitions] FOREIGN KEY([organisationFifaId]) REFERENCES [comet].[organisations] ([organisationFifaId])
GO

ALTER TABLE [comet].[competitions] CHECK CONSTRAINT [fk_organisations_competitions]
GO

CREATE TABLE [comet].[facilities](
	[facilityFifaId] [int] NOT NULL,
	[organisationFifaId] [int] NULL,
	[parentFacilityFifaId] [int] NULL,
	[status] [varchar](100) NULL,
	[internationalName] [varchar](100) NULL,
	[internationalShortName] [varchar](100) NULL,
	[town] [varchar](100) NULL,
	[address] [varchar](100) NULL,
	[webAddress] [varchar](100) NULL,
	[email] [varchar](100) NULL,
	[phone] [varchar](100) NULL,
	[fax] [varchar](100) NULL,
	[capacity] [int] NULL,
	[discipline] [varchar](100) NULL,
	[groundNature] [varchar](100) NULL,
	[latitude] [varchar](100) NULL,
	[longitude] [varchar](100) NULL,
	[length] [int] NULL,
	[orderNumber] [int] NULL,
	[width] [int] NULL,
	[lastUpdate] [datetime] NULL,
 CONSTRAINT [pk_facilities] PRIMARY KEY CLUSTERED([facilityFifaId] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]) ON [PRIMARY]
GO

ALTER TABLE [comet].[facilities] WITH CHECK ADD CONSTRAINT [fk_organisations_facilities] FOREIGN KEY([organisationFifaId]) REFERENCES [comet].[organisations] ([organisationFifaId])
GO

ALTER TABLE [comet].[facilities] CHECK CONSTRAINT [fk_organisations_facilities]
GO

ALTER TABLE [comet].[facilities] WITH CHECK ADD CONSTRAINT [fk_facilities_facilities] FOREIGN KEY([parentFacilityFifaId]) REFERENCES [comet].[facilities] ([facilityFifaId])
GO

ALTER TABLE [comet].[facilities] CHECK CONSTRAINT [fk_facilities_facilities]
GO

CREATE TABLE [comet].[teams](
	[teamFifaId] [int] NOT NULL,
	[organisationFifaId] [int] NULL,
	[facilityFifaId] [int] NULL,
	[status] [varchar](100) NULL,
	[internationalName] [varchar](100) NULL,
	[internationalShortName] [varchar](100) NULL,
	[organisationNature] [varchar](100) NULL,
	[country] [varchar](100) NULL,
	[region] [varchar](100) NULL,
	[town] [varchar](100) NULL,
	[postalCode] [varchar](100) NULL,
	[lastUpdate] [datetime] NULL,
 CONSTRAINT [pk_teams] PRIMARY KEY CLUSTERED([teamFifaId] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]) ON [PRIMARY]
GO

ALTER TABLE [comet].[teams] WITH CHECK ADD CONSTRAINT [fk_organisations_teams] FOREIGN KEY([organisationFifaId]) REFERENCES [comet].[organisations] ([organisationFifaId])
GO

ALTER TABLE [comet].[teams] CHECK CONSTRAINT [fk_organisations_teams]
GO

ALTER TABLE [comet].[teams] WITH CHECK ADD CONSTRAINT [fk_facilities_teams] FOREIGN KEY([facilityFifaId]) REFERENCES [comet].[facilities] ([facilityFifaId])
GO

ALTER TABLE [comet].[teams] CHECK CONSTRAINT [fk_facilities_teams]
GO

CREATE TABLE [comet].[players](
	[playerFifaId] [int] NOT NULL,
	[internationalFirstName] [varchar](100) NULL,
	[internationalLastName] [varchar](100) NULL,
	[countryOfBirth] [varchar](100) NULL,
	[countryOfBirthFIFA] [varchar](100) NULL,
	[dateOfBirth] [date] NULL,
	[gender] [varchar](100) NULL,
	[homegrown] [int] NULL,
	[national_team] [varchar](100) NULL,
	[nationality] [varchar](100) NULL,
	[nationalityFIFA] [varchar](100) NULL,
	[place] [varchar](100) NULL,
	[placeOfBirth] [varchar](100) NULL,
	[playerPosition] [varchar](100) NULL,
	[regionOfBirth] [varchar](100) NULL,
	[rowNumber] [int] NULL,
	[lastUpdate] [datetime] NULL,
 CONSTRAINT [pk_players] PRIMARY KEY CLUSTERED([playerFifaId] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]) ON [PRIMARY]
GO

CREATE TABLE [comet].[persons](
	[personFifaId] [int] NOT NULL,
	[internationalFirstName] [varchar](100) NULL,
	[internationalLastName] [varchar](100) NULL,
	[firstName] [varchar](100) NULL,
	[lastName] [varchar](100) NULL,
	[popularName] [varchar](100) NULL,
	[birthName] [varchar](100) NULL,
	[language] [varchar](100) NULL,
	[title] [varchar](100) NULL,
--	[role] [varchar](100) NULL,
--	[cometRoleName] [varchar](100) NULL,
--	[cometRoleNameKey] [varchar](100) NULL,
	[countryOfBirth] [varchar](100) NULL,
	[countryOfBirthFIFA] [varchar](100) NULL,
	[regionOfBirth] [varchar](100) NULL,
	[placeOfBirth] [varchar](100) NULL,
	[dateOfBirth] [date] NULL,
	[gender] [varchar](100) NULL,
	[homegrown] [int] NULL,
	[national_team] [varchar](100) NULL,
	[nationality] [varchar](100) NULL,
	[nationalityFIFA] [varchar](100) NULL,
	[place] [varchar](100) NULL,
	[playerPosition] [varchar](100) NULL,
	[rowNumber] [int] NULL,
	[lastUpdate] [datetime] NULL,
 CONSTRAINT [pk_persons] PRIMARY KEY CLUSTERED([personFifaId] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]) ON [PRIMARY]
GO

CREATE TABLE [comet].[matches](
	[matchFifaId] [int] NOT NULL,
	[competitionFifaId] [int] NULL,
	[facilityFifaId] [int] NULL,
	[status] [varchar](100) NULL,
	[attendance] [int] NULL,
	[dateTimeLocal] [datetime] NULL,
	[matchDay] [int] NULL,
	[matchDayDesc] [varchar](100) NULL,
	[matchOrderNumber] [int] NULL,
	[resultSupplement] [varchar](100) NULL,
	[resultSupplementAway] [int] NULL,
	[resultSupplementHome] [int] NULL,
	[lastUpdate] [datetime] NULL,
 CONSTRAINT [pk_matches] PRIMARY KEY CLUSTERED([matchFifaId] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]) ON [PRIMARY]
GO

ALTER TABLE [comet].[matches] WITH CHECK ADD CONSTRAINT [fk_competitions_matches] FOREIGN KEY([competitionFifaId]) REFERENCES [comet].[competitions] ([competitionFifaId])
GO

ALTER TABLE [comet].[matches] CHECK CONSTRAINT [fk_competitions_matches]
GO

ALTER TABLE [comet].[matches] WITH CHECK ADD CONSTRAINT [fk_facilities_matches] FOREIGN KEY([facilityFifaId]) REFERENCES [comet].[facilities] ([facilityFifaId])
GO

ALTER TABLE [comet].[matches] CHECK CONSTRAINT [fk_facilities_matches]
GO

CREATE TABLE [comet].[competitions_teams](
	[competitionFifaId] [int] NOT NULL,
	[teamFifaId] [int] NOT NULL,
	[lastUpdate] [datetime] NULL,
 CONSTRAINT [pk_competitions_teams] PRIMARY KEY CLUSTERED([competitionFifaId] ASC, [teamFifaId] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]) ON [PRIMARY]
GO

ALTER TABLE [comet].[competitions_teams] WITH CHECK ADD CONSTRAINT [fk_competitions_competitions_teams] FOREIGN KEY([competitionFifaId]) REFERENCES [comet].[competitions] ([competitionFifaId])
GO

ALTER TABLE [comet].[competitions_teams] CHECK CONSTRAINT [fk_competitions_competitions_teams]
GO

ALTER TABLE [comet].[competitions_teams] WITH CHECK ADD CONSTRAINT [fk_teams_competitions_teams] FOREIGN KEY([teamFifaId]) REFERENCES [comet].[teams] ([teamFifaId])
GO

ALTER TABLE [comet].[competitions_teams] CHECK CONSTRAINT [fk_teams_competitions_teams]
GO

CREATE TABLE [comet].[competitions_teams_players](
	[competitionFifaId] [int] NOT NULL,
	[teamFifaId] [int] NOT NULL,
	[playerFifaId] [int] NOT NULL,
	[lastUpdate] [datetime] NULL,
 CONSTRAINT [pk_competitions_teams_players] PRIMARY KEY CLUSTERED([competitionFifaId] ASC, [teamFifaId] ASC, [playerFifaId] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]) ON [PRIMARY]
GO

ALTER TABLE [comet].[competitions_teams_players] WITH CHECK ADD CONSTRAINT [fk_competitions_teams_competitions_teams_players] FOREIGN KEY([competitionFifaId], [teamFifaId]) REFERENCES [comet].[competitions_teams] ([competitionFifaId], [teamFifaId])
GO

ALTER TABLE [comet].[competitions_teams_players] CHECK CONSTRAINT [fk_competitions_teams_competitions_teams_players]
GO

ALTER TABLE [comet].[competitions_teams_players] WITH CHECK ADD CONSTRAINT [fk_players_competitions_teams_players] FOREIGN KEY([playerFifaId]) REFERENCES [comet].[players] ([playerFifaId])
GO

ALTER TABLE [comet].[competitions_teams_players] CHECK CONSTRAINT [fk_players_competitions_teams_players]
GO

CREATE TABLE [comet].[matches_teams](
	[matchFifaId] [int] NOT NULL,
	[teamFifaId] [int] NOT NULL,
	[team_nature] [varchar](100) NULL,
	[lastUpdate] [datetime] NULL,
 CONSTRAINT [pk_matches_teams] PRIMARY KEY CLUSTERED([matchFifaId] ASC,	[teamFifaId] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]) ON [PRIMARY]
GO

ALTER TABLE [comet].[matches_teams] WITH CHECK ADD CONSTRAINT [fk_matches_matches_teams] FOREIGN KEY([matchFifaId]) REFERENCES [comet].[matches] ([matchFifaId])
GO

ALTER TABLE [comet].[matches_teams] CHECK CONSTRAINT [fk_matches_matches_teams]
GO

ALTER TABLE [comet].[matches_teams] WITH CHECK ADD CONSTRAINT [fk_teams_matches_teams] FOREIGN KEY([teamFifaId]) REFERENCES [comet].[teams] ([teamFifaId])
GO

ALTER TABLE [comet].[matches_teams] CHECK CONSTRAINT [fk_teams_matches_teams]
GO
/*
CREATE TABLE [comet].[matches_referees](
	[matchFifaId] [int] NOT NULL,
	[refereeFifaId] [int] NOT NULL,
	[personFifaId] [int] NULL,
	[personName] [varchar](100) NULL,
	[localPersonName] [varchar](100) NULL,
	[role] [varchar](100) NULL,
	[roleDescription] [varchar](100) NULL,
	[cometRoleName] [varchar](100) NULL,
	[cometRoleNameKey] [varchar](100) NULL,
	[lastUpdate] [datetime] NULL,
 CONSTRAINT [pk_matches_officials] PRIMARY KEY CLUSTERED([matchFifaId] ASC,	[refereeFifaId] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]) ON [PRIMARY]
GO

ALTER TABLE [comet].[matches_officials]  WITH CHECK ADD CONSTRAINT [fk_matches] FOREIGN KEY([matchFifaId]) REFERENCES [comet].[matches] ([matchFifaId])
GO

ALTER TABLE [comet].[matches_officials] CHECK CONSTRAINT [fk_matches]
GO
*/
INSERT INTO [comet].[organisations] ([organisationFifaId], [organisationName], [organisationNature], [organisationShortName], [lastUpdate]) VALUES (1, 'DEFAULT', 'DEFAULT', 'DEFAULT', GETDATE())
GO

INSERT INTO [comet].[organisations] ([organisationFifaId], [organisationName], [organisationNature], [organisationShortName], [lastUpdate]) VALUES (39393, 'CONFEDERACIÓN SUDAMERICANA DE FÚTBOL', 'CONMEBOL', 'CONMEBOL', GETDATE())
GO