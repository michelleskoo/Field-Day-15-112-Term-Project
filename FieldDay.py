import cv2
import numpy as np
import requests
import io
import os
import ast
import csv
from PIL import Image
from shapely.geometry import Point
from shapely.geometry import Polygon
import math, copy, random
from cmu_112_graphics import *

class HomescreenMode(Mode):
    def appStarted(mode):
        ball = mode.loadImage("golfball.png")
        mode.ball = mode.scaleImage(ball, 1/8)
        play = mode.loadImage("golfball.png")
        mode.play = mode.scaleImage(play, 1/2)
        homescreen = mode.loadImage("course.png")
        mode.homescreen = homescreen.transpose(Image.FLIP_LEFT_RIGHT)
        
        mode.playx0 = mode.width*2/5
        mode.playy0 = mode.height*3/7
        mode.playx1 = mode.width*3/5
        mode.playy1 = mode.height*3/4

        mode.aboutx0 = mode.width*2/3
        mode.abouty0 = mode.height*3/7
        mode.aboutx1 = mode.width*5/6
        mode.abouty1 = mode.height*3/4
        
        mode.statisticsx0 = mode.width/6
        mode.statisticsy0 = mode.height*3/7
        mode.statisticsx1 = mode.width*1/3
        mode.statisticsy1 = mode.height*3/4

    def mousePressed(mode, event):
        #coodinates to activate playMode
        if ((event.x >= mode.playx0 and event.x <= mode.playx1) and
			(event.y >= mode.playy0 and event.y <= mode.playy1)):
            mode.app.setActiveMode(mode.app.playMode)
        #coordinates to activiate statisticsMode
        elif ((event.x >= mode.statisticsx0 and event.x <= mode.statisticsx1) and
			  (event.y >= mode.statisticsy0 and event.y <= mode.statisticsy1)):
              mode.app.setActiveMode(mode.app.statsMode)
        elif ((event.x >= mode.aboutx0 and event.x <= mode.aboutx1) and
			  (event.y >= mode.abouty0 and event.y <= mode.abouty1)):
              mode.app.setActiveMode(mode.app.aboutMode)
    
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.homescreen))
        canvas.create_text(mode.width/2-10, mode.height/4-10, text = "FIELD  DAY", font = "Impact 180 bold",
						   fill = "white")
        canvas.create_text(mode.width/2, mode.height/4, text = "FIELD  DAY", font = "Impact 180 bold", fill = "midnight blue")
        canvas.create_image(mode.width/2 + 40, mode.height/4, image = ImageTk.PhotoImage(mode.ball))
        canvas.create_rectangle(mode.width/6, mode.height/3+20, mode.width*5/6, mode.height/3+30, fill = "black", width = 0)
        canvas.create_rectangle(0, 0, mode.width, mode.height, 
								fill = "", width = 50, outline = "linen")
        
        font = "Impact 45 bold"
        #to draw play button
        canvas.create_image(mode.width/2, mode.height*3/5, image = ImageTk.PhotoImage(mode.play))
        canvas.create_text(mode.width/2, mode.height*3/5, text = "Play", font = font)
        #to draw stats button
        canvas.create_image(mode.width/4, mode.height*3/5, image = ImageTk.PhotoImage(mode.play))
        canvas.create_text(mode.width/4, mode.height*3/5, text = "Stats", font = font)
        #to draw about button
        canvas.create_image(mode.width*3/4, mode.height*3/5, image = ImageTk.PhotoImage(mode.play))
        canvas.create_text(mode.width*3/4, mode.height*3/5, text = "About", font = font)

class AboutMode(Mode):
    def appStarted(mode):
        homescreen = mode.loadImage("course.png")
        mode.homescreen = homescreen.transpose(Image.FLIP_LEFT_RIGHT)
    def keyPressed(mode, event):
        if event.key == "h":
            mode.app.setActiveMode(mode.app.homescreenMode)
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.homescreen))
        canvas.create_rectangle(mode.width/8, mode.height/7, mode.width*7/8, mode.height*6/7, 
								fill = "dark green", width = 20, outline = "linen")
        canvas.create_text(mode.width/2-5, mode.height/7-5, text = "About", 
                               font = "Impact 100 bold", fill = "white")
        canvas.create_text(mode.width/2, mode.height/7, text = "About", 
                               font = "Impact 100 bold")
        canvas.create_text(mode.width/2, mode.height/4, 
                          text = "The perfect app to track your stats real time.", font = "Impact 25 bold")
        canvas.create_text(mode.width/2, mode.height*5/16, 
                          text = "You can keep track of your past rounds", font = "Impact 25 bold", fill = "navy")
        canvas.create_text(mode.width/2, mode.height*3/8, 
                          text = "and watch your score go down!", font = "Impact 25 bold", fill = "navy")
        canvas.create_text(mode.width/2, mode.height*7/16, 
                          text = "To begin: Press “Play” and Select your course ", font = "Impact 25 bold")
        canvas.create_text(mode.width/2, mode.height/2, 
                          text = "or add your home course into the database!", font = "Impact 25 bold")
        canvas.create_text(mode.width/2, mode.height*9/16, 
                          text = "After your round: Go to “Stats” and discover which", font = "Impact 25 bold", fill = "navy")
        canvas.create_text(mode.width/2, mode.height*5/8, text = "parts of your game need work!", font = "Impact 25 bold", fill = "navy")
        canvas.create_text(mode.width*2/3-5, mode.height*3/4-5, 
                          text = "Good Luck and Play Well!\n           <3 M", font = "Impact 20 bold", fill = "navy")
        canvas.create_text(mode.width*2/3, mode.height*3/4, 
                          text = "Good Luck and Play Well!\n           <3 M", font = "Impact 20 bold", fill = "white")

class PlayMode(Mode):
    def appStarted(mode):
        ball = mode.loadImage("golfball.png")
        mode.ball = mode.scaleImage(ball, 1/4)
        mode.ball2 = mode.scaleImage(ball, 1/6)
        homescreen = mode.loadImage("course.png")
        mode.homescreen = homescreen.transpose(Image.FLIP_LEFT_RIGHT)
        banner = mode.loadImage("banners.png")
        mode.banner = mode.scaleImage(banner, 2/5)
        
        mode.roundx0 = mode.width/4
        mode.roundy0 = mode.height/3
        mode.roundx1 = mode.width*3/4
        mode.roundy1 = mode.height*2/5

        mode.addx0 = mode.width/4
        mode.addy0 = mode.height*3/5
        mode.addx1 = mode.width*3/4
        mode.addy1 = mode.height*2/3
        
        mode.courses = []
        mode.users = []
        mode.course = None
        mode.date = None
        mode.username = None
        mode.imageMargins = 15
        mode.golfCourseName = None
        mode.foundCourse = False
        mode.dateEntered = False
        mode.usernameEntered = False
        mode.play = False
        
        mode.par = {}
        mode.greenCoordinates = {}
        mode.fairwayCoordinates = {}
        
        mode.putts = {}
        mode.totalGreens = 0
        mode.hitGreens = 0
        mode.totalFairways = 0
        mode.hitFairways = 0
        mode.totalStrokesGained = {}
        
        mode.hole = 1
        mode.csvInformation = []
        mode.courseInformation = {}
        mode.rows = None
        mode.cols = None
        mode.heightMargins = None
        mode.widthMargins = None
        
        mode.playing = True
        mode.aiming = False
        mode.aimPoint = None
        mode.holeLocation = None

        mode.playerPath = {}
        mode.currPlayerPath = []
        mode.distance = []
        mode.image = None
        
        mode.summary = False
        mode.score = 0
        mode.todaysStrokesGained = 0
        mode.todaysStats = {}
        
    def keyPressed(mode, event):
        if event.key == "n" and mode.play:
            if mode.hole == 18:
                coordinates = mode.getImageCoordinates(mode.currPlayerPath)
                mode.playerPath[mode.hole] = coordinates
                if mode.fairwayCoordinates[mode.hole] != []:
                    mode.checkFairways()
                mode.checkGreens()
                mode.getTotalStrokesGained()
                mode.countPutts()
                mode.getTotalScore()
                mode.sumTotalStrokesGained()
                mode.play = False
                mode.summary = True
                mode.saveStats()
                mode.makeStatsToCsv()
            else:
                mode.playerPath[mode.hole] = mode.currPlayerPath
                if mode.fairwayCoordinates[mode.hole] != []:
                    mode.checkFairways()
                mode.checkGreens()
                mode.countPutts()
                mode.getTotalStrokesGained()
                mode.currPlayerPath = []
                mode.distance = []
                mode.hole += 1
                mode.getImage()
                mode.getHoleDimensions()
                mode.getMargins()
                mode.getListHoleCoordinates()
                mode.playing = True
                distance = mode.getUserInput("Enter Starting Hole Distance from Tee")
                while distance == None:
                        distance = mode.getUserInput("Enter a Distance")
                mode.distance.append(int(distance))
        if event.key == "a" and mode.play:
            mode.playing = False
            mode.aiming = True
        if event.key == "b" and mode.play:
            mode.aiming = False
            mode.playing = True
            mode.holeLocation = None
            mode.aimPoint = None
        if event.key == "d" and mode.currPlayerPath != [] and mode.play:
            mode.currPlayerPath.pop()
            mode.distance.pop()
        if event.key == "h":
            mode.appStarted()
            mode.app.setActiveMode(mode.app.homescreenMode)
    
    def mousePressed(mode, event):
        if mode.play:
            if mode.aiming:
                mode.holeLocation = (event.x, event.y)
                mode.aimPoint = mode.getOptimization(mode.holeLocation)
            elif mode.playing:
                distance = mode.getUserInput("Enter Distance to Hole")
                while distance == None:
                    distance = mode.getUserInput("Enter a Distance")
                mode.distance.append(int(distance))
                mode.currPlayerPath.append((event.x, event.y))
        else:
            if ((event.x >= mode.roundx0 and event.x <= mode.roundx1) and
			(event.y >= mode.roundy0 and event.y <= mode.roundy1)):
                if not mode.usernameEntered:
                    username = mode.getUserInput("Enter or create username")
                    if username == None:
                        mode.username = username
                    else:
                        mode.username = username
                        mode.usernameEntered = True
                        mode.getCourseList()
                        golfCourseName = mode.getUserInput("Enter Your Golf Course Name")
                        if golfCourseName == None:
                            mode.golfCourseName = golfCourseName
                        elif golfCourseName not in mode.courses:
                            golfCourseName = mode.getUserInput("Golf Course not in Database.\nCancel and Add Course\nor Choose New Course.")
                        else:
                            mode.golfCourseName = golfCourseName
                            mode.foundCourse = True
                        date = mode.getUserInput("Enter Today's Date (MM/DD/YYYY)")
                        if date == None:
                            mode.date = date
                        else:
                            mode.date = date
                            mode.dateEntered = True
                            mode.getImage()
                            mode.getHoleDimensions()
                            mode.getMargins()
                            mode.csvToDictionary()
                            mode.getListHoleCoordinates()
                            distance = mode.getUserInput("Enter Starting Hole Distance from Tee")
                            while distance == None:
                                distance = mode.getUserInput("Enter a Distance")
                            mode.distance.append(int(distance))
                            mode.play = True
            elif ((event.x >= mode.addx0 and event.x <= mode.addx1) and
			(event.y >= mode.addy0 and event.y <= mode.addy1)):
                mode.app.setActiveMode(mode.app.course)

    def getDistance(mode, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return ((y2-y1)**2 + (x2-x1)**2)**0.5

    #because I do not have enough data about the shot angle or trajectory, which is empirical data gathered from a launch monitor
    #I made an appoximation that can later be more accurate to fit the ellipse shape of an iron/driver
    def getProbability(mode, point, center):
        x1, y1 = point
        x2, y2 = center
        x = abs(x2-x1)
        y = abs(y2-y1)
        ellipse = -(x/14.5)**2 - (y/7.25)**2
        return math.exp(ellipse)

    def getImageCoordinate(mode, coordinates):
        x, y = coordinates
        newX, newY = x - mode.widthMargins,  y - mode.heightMargins
        return newX, newY

    def getExpectedBaseline(mode, center, hole):
        sum = 0
        center = mode.getImageCoordinate(center)
        for x in range(mode.cols):
            for y in range(mode.rows//2):
                point = (x, y)
                probability = mode.getProbability(point, center)
                realPoint = mode.getAppCoordinates(x, y)
                distancePoints = mode.getDistance(center, hole)
                #distance calculated from converting 1.33m/pixel to the scaled image (1.8) and to yards
                distance = 1.45 * distancePoints
                if mode.pointInPolygon(realPoint, mode.greenCoordinates[mode.hole]) == True:
                    baseline = mode.getBaselinePutts(distance)
                else:
                    for j in range(len(mode.fairwayCoordinates[mode.hole])):
                        coordinates = mode.fairwayCoordinates[mode.hole][j]
                        if mode.pointInPolygon(realPoint, coordinates):
                            if distance > 250:
                                baseline = mode.getBaselineTeeFairway(distance)
                            else:
                                baseline = mode.getBaselineFairwayGreen(distance)
                        else:
                            #0.25 is an approximation used because I currently do not have access to the PGA tour's statistics
                            if distance > 250:
                                baseline = mode.getBaselineTeeFairway(distance) + 0.25
                            else:
                                baseline = mode.getBaselineFairwayGreen(distance) + 0.25
                addition = baseline * probability
                sum += addition
        return sum

    def getOptimization(mode, aim):
        hole = mode.holeLocation
        minimum = aim
        x, y = aim
        s = mode.getExpectedBaseline(aim, hole)
        temp = 0
        #from cmu-112: https://www.cs.cmu.edu/~112/notes/unit5-case-studies.html#connect4
        dirs = [ (-1, -1), (-1, 0), (-1, +1),
                 ( 0, -1),          ( 0, +1),
                 (+1, -1), (+1, 0), (+1, +1) ]
        for dir in dirs:
            x += dir[0]
            y += dir[1]
            point = (x, y)
            temp = mode.getExpectedBaseline(point, hole)
            if temp < s:
                minimum = point
        if minimum == aim:
            return aim
        else:
            return mode.getOptimization(minimum)

    def countPutts(mode):
        count = 0
        coordinates = mode.greenCoordinates[mode.hole]
        for point in mode.currPlayerPath:
            if mode.pointInPolygon(point, coordinates):
                count += 1
        mode.putts[mode.hole] = count - 1
    
    def countTotalPutts(mode):
        count = 0
        for hole in mode.putts:
            count += mode.putts[hole]
        return count
    
    def checkGreens(mode):
        mode.totalGreens += 1
        if mode.pointInGreen():
            mode.hitGreens += 1
    
    def pointInGreen(mode):
        coordinates = mode.greenCoordinates[mode.hole]
        if mode.par[mode.hole] == "5":
            found = False
            for i in range(1, 3):
                point = mode.currPlayerPath[i]
                check = mode.pointInPolygon(point, coordinates)
                if check == True:
                    found = True
            return found
        elif mode.par[mode.hole] == "4":
            point = mode.currPlayerPath[1]
            return mode.pointInPolygon(point, coordinates)
        else:
            point = mode.currPlayerPath[0]
            return mode.pointInPolygon(point, coordinates)
    
    def checkFairways(mode):
        mode.totalFairways += 1
        for i in range(len(mode.fairwayCoordinates[mode.hole])):
            coordinates = mode.fairwayCoordinates[mode.hole][i]
            if mode.pointInFairway(coordinates, 0):
                mode.hitFairways += 1
    
    def pointInFairway(mode, coordinates, index):
		#return True or False after checking point
        point = mode.currPlayerPath[index]
        return mode.pointInPolygon(point, coordinates)
    
    def pointInPolygon(mode, point, coordinates):
        intersect = 0
        xp, yp = point
        xl, yl = 0, yp
        edges = mode.getEdges(coordinates)
        for edge in edges:
            x1, y1 = edge[0]
            x2, y2 = edge[1]
            if mode.yTest(yp, y1, y2):
                if mode.xTest(xl, xp, x1, x2):
                    x = mode.getXIntercept(xl, yl, xp, yp, x1, y1, x2, y2)
                    if x >= xl and x <= xp:
                        intersect += 1
        
        if intersect % 2 == 1:
            return True
        #an even amount of intersections --> point is outside of polygon
        else:
            return False

    #to test if of the line segments will intersect given the y-parameters
    def yTest(mode, yp, y1, y2):
        if y1 <= yp and y2 > yp:
            return True
        elif y2 <= yp and y1 > yp:
            return True
        else:
            return False
    
    #tests that at least one of the x-coordinates is in the horizontal ray
    def xTest(mode, xl, xp, x1, x2):
        if xl <= x1 and xp >= x1:
            return True
        elif xl <= x2 and xp >= x2:
            return True
        else:
            return False
    
    def getXIntercept(mode, xl, yl, xp, yp, x1, y1, x2, y2):
        if x1 == x2:
            return x1
        else:
            m = (y2 - y1)/(x2 - x1)
            b = y1 - m * x1
            x = (yp - b) / m
            return x
    
    def getEdges(mode, coordinates):
		#return list of pairs of points that make up the edges of the polygon
        last = None
        first = None
        edges = []
        for coordinate in coordinates:
            curr = coordinate
            if last == None:
                last = curr
                first = curr
            else:
                edges.append((last, curr))
                last = curr
        edges.append((last, first))
        return edges
    
    def getImageCoordinates(mode, coordinates):
        updatedCoordinates = []
        for coordinate in coordinates:
            x, y = coordinate
            newX, newY = x - mode.widthMargins,  y - mode.heightMargins
            updatedCoordinates.append((newX, newY))
        return updatedCoordinates
    
    def getMargins(mode):
        mode.heightMargins = (mode.height - mode.rows)/2
        mode.widthMargins = (mode.width - mode.cols)/2
    
    def getHoleDimensions(mode):
        image = mode.image
        w, h = image.size
        mode.rows = h
        mode.cols = w
        
    def getListHoleCoordinates(mode):
        updatedG = []
        for coordinate in mode.greenCoordinates[mode.hole]:
            x, y = coordinate
            newX, newY = mode.getAppCoordinates(x, y)
            updatedG.append((newX, newY))
        mode.greenCoordinates[mode.hole] = updatedG
        
        if len(mode.fairwayCoordinates[mode.hole]) == 1:
            updatedF = []
            for coordinate in mode.fairwayCoordinates[mode.hole][0]:
                x, y = coordinate
                newX, newY = mode.getAppCoordinates(x, y)
                updatedF.append((newX, newY))
            updatedF = [updatedF]
        else:
            updatedF = []
            for i in range(len(mode.fairwayCoordinates[mode.hole])):
                currFairway = []
                for coordinate in mode.fairwayCoordinates[mode.hole][i]:
                    x, y = coordinate
                    newX, newY = mode.getAppCoordinates(x, y)
                    currFairway.append((newX, newY))
                updatedF.append((currFairway))
        mode.fairwayCoordinates[mode.hole]= updatedF

	#methods/code for ast: https://www.geeksforgeeks.org/python-convert-a-string-representation-of-list-into-list/
    def stringToList(mode, s):
        return ast.literal_eval(s)
    
    def getAppCoordinates(mode, x, y):
        newX, newY = x + mode.widthMargins,  y + mode.heightMargins
        return newX, newY

	#code to use DictReader: https://courses.cs.washington.edu/courses/cse140/13wi/csv-parsing.html
    def csvToDictionary(mode):
        input_file = csv.DictReader(open(f'{mode.golfCourseName}Information.csv'))
        for row in input_file:
            mode.csvInformation.append(dict(row))
        
        count = 1
        for hole in mode.csvInformation:
            green = mode.stringToList(hole['green coordinates'])
            fairway = mode.stringToList(hole['fairway coordinates'])
            mode.par[count] = hole["par"]
            mode.greenCoordinates[count] = green
            mode.fairwayCoordinates[count] = fairway
            count += 1
    
    def getImage(mode):
        mode.image = mode.loadImage(f'{mode.golfCourseName}Hole{mode.hole}.png')
    
    def getTotalScore(mode):
        score = 0
        for lst in mode.playerPath:
            score += len(mode.playerPath[lst])
        mode.score = score

    #Baseline formula calculated through an excek fit of the PGA tour's baseline data
    #This was used because all of the PGA tour data is not avaliable to the public
    def getBaselinePutts(mode, distance):
        baseline = 0.795 + 0.349 * math.log1p(distance)
        return baseline

    def getBaselineTeeFairway(mode, distance):
        baseline = 2.37 + (0.00351*distance) + (0.00000272*(distance**2)) 
        return baseline

    def getBaselineFairwayGreen(mode, distance):
        baseline = 2.23 + (0.00562*distance) - (0.00000353 * (distance**2))
        return baseline

    def getTotalStrokesGained(mode):
        sum = 0
        lastShot = None
        for i in range(len(mode.currPlayerPath)):
            point = mode.currPlayerPath[i]
            currShot = 0
            strokesGained = 0
            distance = mode.distance[i]
            if lastShot == None:
                lastShot = mode.getBaselineTeeFairway(distance)
            elif mode.pointInPolygon(point, mode.greenCoordinates[mode.hole]) == True:
                currShot = mode.getBaselinePutts(distance)
                strokesGained = (lastShot - currShot) - 1
                lastShot = currShot
                sum += strokesGained
            elif mode.par[mode.hole] == 3:
                if distance > 250:
                        currShot = mode.getBaselineTeeFairway(distance)
                else:
                        currShot = mode.getBaselineFairwayGreen(distance)
                strokesGained = (lastShot - currShot) - 1
                sum += strokesGained
            else:
                for j in range(len(mode.fairwayCoordinates[mode.hole])):
                    if mode.pointInFairway(mode.fairwayCoordinates[mode.hole][j], i):
                        if distance > 250:
                            currShot = mode.getBaselineTeeFairway(distance)
                        else:
                            currShot = mode.getBaselineFairwayGreen(distance)
                        strokesGained = (lastShot - currShot) - 1
                        sum += strokesGained
                    else:
                        #0.25 is an approximation used because I currently do not have access to the PGA tour's statistics
                        if distance > 250:
                            currShot = mode.getBaselineTeeFairway(distance) + 0.25
                        else:
                            currShot = mode.getBaselineFairwayGreen(distance) + 0.25
                        strokesGained = (lastShot - currShot) - 1
                        sum += strokesGained
                lastShot = currShot
        mode.totalStrokesGained[mode.hole] = sum  

    def sumTotalStrokesGained(mode):
        print(mode.totalStrokesGained)
        count = 0
        for hole in mode.totalStrokesGained:
            count += mode.totalStrokesGained[mode.hole]
        mode.todaysStrokesGained = count 
    
    def saveStats(mode):
        stats = {}
        stats["date"] = mode.date
        stats["score"] = mode.score
        stats["greens"] = mode.hitGreens
        stats["fairways"] = mode.hitFairways
        stats["putts"] = mode.countTotalPutts()
        stats["strokes gained"] = mode.todaysStrokesGained
        mode.todaysStats = stats

	#notes/code to create csv file from dictionary from: 
    # https://www.tutorialspoint.com/How-to-save-a-Python-Dictionary-to-CSV-file
    def makeStatsToCsv(mode):
        columnNames = ["date", "score", "greens", "fairways", "putts", "strokes gained"]
        csvFile = f'{mode.username}Stats.csv'
        try:
            mode.getUserList()
            if mode.username in mode.users:
                with open(csvFile, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=columnNames)
                    writer.writeheader()
                    writer.writerow(mode.todaysStats)
            else:
                mode.addUsers(mode.username)
                with open(csvFile, 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=columnNames)
                    writer.writeheader()
                    writer.writerow(mode.todaysStats)
        except IOError:
            print("I/O error")
    
    def getCourseList(mode):
        file = open("courses.txt", "r")
        if file == "":
            mode.courses = []
        else:
            for line in file:
                for course in line.split(","):
                    mode.courses.append(course)
        file.close()
    
    def getUserList(mode):
        wfile = open("users.txt", "a")
        wfile.close()
        rfile = open("users.txt", "r")
        if rfile == "":
            mode.users = []
        else:
            for line in rfile:
                for user in line.split(","):
                    mode.users.append(user)
        rfile.close()
    
    def addUsers(mode, username):
        users = "users.txt"
        with open(users, "a") as text_file:
           text_file.write(mode.username + ",")

    def drawShots(mode, canvas):
        for i in range(len(mode.currPlayerPath)):
            x, y = mode.currPlayerPath[i]
            canvas.create_text(x, y, text = f'{i+1}', font = "Impact 12 bold", fill = "black")
            canvas.create_text(x, y, text = f'{i+1}', font = "Impact 10 bold", fill = "white")
    
    def drawOptimalAim(mode, canvas):
        if mode.holeLocation == None:
            canvas.create_text(mode.width/2, mode.height/6, text = "Press hole location to get aim point!", font = "Impact 20", fill = "navy")
        if mode.aimPoint != None:
            canvas.create_line(mode.currPlayerPath[-1], mode.aimPoint, width = 1, fill = "red")
            canvas.create_text(mode.width/2, mode.height/6, text = "Press 'b' to go back!", font = "Impact 20", fill = "navy")

    def drawDirections(mode, canvas):
        canvas.create_text(mode.width/2, mode.height/6, text = "Press 'd' to delete shot.", font = "Impact 20", fill = "navy")
        canvas.create_text(mode.width/2, mode.height/7, text = "Press 'a' to get optimal aim point!", font = "Impact 20", fill = "navy")

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.homescreen))
        
        if not mode.play and not mode.summary:
            canvas.create_rectangle(mode.width/8, mode.height/5, mode.width*7/8, mode.height*4/5, 
								fill = "dark green", width = 20, outline = "linen")
            x0 = mode.roundx0
            y0 = mode.roundy0
            x1 = mode.roundx1
            y1 = mode.roundy1
            canvas.create_rectangle(x0, y0, x1, y1, fill = "linen", width = 0)
            canvas.create_text(mode.width/2, mode.height*2/5-25, text = "+ Start New Round", font = "Impact 40")
            
            x01 = mode.addx0
            y01 = mode.addy0
            x11 = mode.addx1
            y11 = mode.addy1
            canvas.create_rectangle(x01, y01, x11, y11, fill = "linen", width = 0)
            canvas.create_text(mode.width/2, mode.height*3/5 + 25, text = "Add More Courses", font = "Impact 40")
            
            canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.ball))
            canvas.create_text(mode.width/2-5, mode.height/2-5, text = "F D", font = "Impact 40 bold", fill = "linen")
            canvas.create_text(mode.width/2, mode.height/2, text = "F D", font = "Impact 40 bold", fill = "navy")
        
        if mode.play:
            canvas.create_rectangle(mode.width/10, mode.height/10, mode.width*9/10, mode.height*9/10, 
								fill = "dark green", width = 20, outline = "linen")
            x0 = mode.widthMargins - mode.imageMargins
            y0 = mode.heightMargins - mode.imageMargins
            x1 = mode.cols + mode.imageMargins + mode.widthMargins
            y1 = mode.rows + mode.imageMargins + mode.heightMargins
            canvas.create_rectangle(x0, y0, x1, y1, fill = "linen", width = 5)

            canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.image))
            mode.drawShots(canvas)

            canvas.create_image(mode.width/10, mode.height/10, image = ImageTk.PhotoImage(mode.ball))
            canvas.create_text(mode.width/10, mode.height/10, text = f'HOLE\n    {mode.hole}', font = "Impact 25 bold")
            canvas.create_image(mode.width*7/8-10, mode.height/9, image = ImageTk.PhotoImage(mode.banner))
            canvas.create_image(mode.width*7/9 + 10, mode.height/9+10, image = ImageTk.PhotoImage(mode.ball2))
            canvas.create_text(mode.width*7/8, mode.height/9, text = f'Par {mode.par[mode.hole]}', font = "Impact 30 bold")
            if mode.aiming:
                mode.drawOptimalAim(canvas)
            elif mode.playing:
                mode.drawDirections(canvas)
        
        if mode.summary:
            canvas.create_rectangle(mode.width/8, mode.height/8, mode.width*7/8, mode.height*7/8, 
								fill = "dark green", width = 20, outline = "linen")
            canvas.create_text(mode.width/2-5, mode.height/4-5, text = "SUMMARY", font = "Impact 100 bold", fill = "white")
            canvas.create_text(mode.width/2, mode.height/4, text = "SUMMARY", font = "Impact 100 bold")
            canvas.create_text(mode.width/2, mode.height/3, text = f'Score: {mode.score}', font = "Impact 40 bold")
            canvas.create_text(mode.width/2, mode.height/2, text = f'Greens In Regulation: {mode.hitGreens}/{mode.totalGreens}', font = "Impact 40 bold")
            canvas.create_text(mode.width/2, mode.height*2/3, text = f'Fairways: {mode.hitFairways}/{mode.totalFairways}', font = "Impact 40 bold")
        canvas.create_rectangle(0, 0, mode.width, mode.height, 
								fill = "", width = 50, outline = "linen")

class StatsMode(Mode):
    def appStarted(mode):
        ball = mode.loadImage("golfball.png")
        mode.ball = mode.scaleImage(ball, 2/3)
        homescreen = mode.loadImage("course.png")
        mode.homescreen = homescreen.transpose(Image.FLIP_LEFT_RIGHT)

        mode.x0 = mode.width/3
        mode.y0 = mode.height/3
        mode.x1 = mode.width*2/3
        mode.y1 = mode.height*2/3

        mode.users = []
        mode.userFound = False
        mode.stats = {}
        mode.username = None
        mode.csvInformation = {}

        mode.scores = []
        mode.greens = []
        mode.fairways = []
        mode.putts = []
        mode.strokesGained = []
    
    def mousePressed(mode, event):
        if not mode.userFound:
            if ((event.x >= mode.x0 and event.x <= mode.x1) and
			    (event.y >= mode.y0 and event.y <= mode.y1)):
                username = mode.getUserInput("Enter Username")
                if username == None:
                    mode.username = username
                else:
                    mode.username = username
                mode.getUsers()
                while mode.username not in mode.users:
                    username = mode.getUserInput("Username not found in Database. Try Again.")
                    if username == None:
                        mode.app.setActiveMode(mode.app.homescreenMode)
                    else:
                        mode.username = username
                else:
                    mode.userFound = True
                mode.csvToDictionary()
                mode.scoringAvg = mode.getAverage(mode.scores)
                mode.scoringSd = mode.getStandardDeviation(mode.scores)
                mode.greensAvg = mode.getAverage(mode.greens)
                mode.fairwaysAvg = mode.getFairwaysPercentageAvg(mode.fairways)
                mode.fairwaysSd = mode.getStandardDeviation(mode.fairways)
                mode.strokesGainedAvg = round(mode.getAverage(mode.strokesGained),2)
                mode.strokesGainedSd = round(mode.getStandardDeviation(mode.strokesGained), 2)
                mode.puttsAvg = mode.getAverage(mode.putts)
                mode.puttsSd = mode.getStandardDeviation(mode.putts)
    
    def keyPressed(mode, event):
        if event.key == "h":
            mode.appStarted()
            mode.app.setActiveMode(mode.app.homescreenMode)
    
    def getUsers(mode):
        file = open("users.txt", "r")
        if file == "":
            mode.users = []
        else:
            for line in file:
                for user in line.split(","):
                    mode.users.append(user)
        file.close()
    
    def getAverage(mode, L):
        sum = 0
        for item in L:
            sum += item
        return sum/len(L)
    
    def getStandardDeviation(mode, L):
        count = len(L)
        mean = mode.getAverage(L)
        differences = []
        for item in L:
            difference = item - mean
            differences.append(difference)
        sumDif = 0
        for num in differences:
            sumDif += (num**2)
        variance = sumDif / count
        return math.sqrt(variance)
    
    def getPercentage(mode, count, total):
        return (count/total) * 100
    
    def getFairwaysPercentageAvg(mode, L):
        percentages = []
        for item in L:
            percentage = mode.getPercentage(item, 14)
            percentages.append(percentage)
        count = 0
        for num in percentages:
            count += num
        return int(count/len(L))

    def csvToDictionary(mode):
        count = 0
        input_file = open(f'{mode.username}Stats.csv')
        for row in input_file:
            if count % 2 == 1:
                stats = row.split(",")
                mode.scores.append(int(stats[1]))
                mode.greens.append(int(stats[2]))
                mode.fairways.append(int(stats[3]))
                mode.putts.append(int(stats[4]))
                sg = stats[5].strip()
                sg = float(sg)
                sg = round(sg,2)
                mode.strokesGained.append(sg)
            count += 1
    def drawScoreStats(mode, canvas):
        canvas.create_text(mode.width/4+40, mode.height/4+40, text = f'{mode.scoringAvg}', 
                               fill = "navy", font = "Impact 160 bold")
        canvas.create_text(mode.width/4+40, mode.height/6, text = f'({mode.scoringSd})', font = "Impact 30 bold")
        canvas.create_text(mode.width/4+35, mode.height/2-35, text = "Scoring Average", font = "Impact 30 bold", fill = "navy")
        canvas.create_text(mode.width/4+40, mode.height/2-30, text = "Scoring Average", font = "Impact 30 bold", fill = "white")

    def drawFairwayStats(mode, canvas):
        canvas.create_text(mode.width*2/3+30, mode.height/4+40, text = f'{mode.fairwaysAvg}%', 
                               fill = "navy", font = "Impact 160 bold")
        canvas.create_text(mode.width*2/3+30, mode.height/6, text = f'({mode.fairwaysSd})', font = "Impact 30 bold")
        canvas.create_text(mode.width*2/3+35, mode.height/2-35, text = "Fairways Hit", font = "Impact 30 bold", fill = "navy")
        canvas.create_text(mode.width*2/3+40, mode.height/2-30, text = "Fairways Hit", font = "Impact 30 bold", fill = "white")

    def drawStrokesGainedStats(mode, canvas):
        canvas.create_text(mode.width/4+40, mode.height*2/3+30, text = f'{mode.strokesGainedAvg}', 
                               fill = "navy", font = "Impact 160 bold")
        canvas.create_text(mode.width/4+40, mode.height*5/6, text = f'({mode.strokesGainedSd})', font = "Impact 30 bold")
        canvas.create_text(mode.width/4+35, mode.height/2+30, text = "Strokes Gained", font = "Impact 30 bold", fill = "navy")
        canvas.create_text(mode.width/4+40, mode.height/2+35, text = "Strokes Gained", font = "Impact 30 bold", fill = "white")

    def drawAveragePutts(mode, canvas):
        canvas.create_text(mode.width*2/3+30, mode.height*2/3+30, text = f'{mode.puttsAvg}', 
                               fill = "navy", font = "Impact 160 bold")
        canvas.create_text(mode.width*2/3+30, mode.height*5/6, text = f'({mode.puttsSd})', font = "Impact 30 bold")
        canvas.create_text(mode.width*2/3+35, mode.height/2+30, text = "Average Putts", font = "Impact 30 bold", fill = "navy")
        canvas.create_text(mode.width*2/3+40, mode.height/2+35, text = "Average Putts", font = "Impact 30 bold", fill = "white")


    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.homescreen))
        if not mode.userFound:
            canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.ball))
            canvas.create_text(mode.width/2, mode.height/2, text = "       Click to \n  Retrieve Stats", font = "Impact 40 bold")
        else:
            canvas.create_rectangle(mode.width/10, mode.height/10, mode.width*9/10, 
									mode.height*9/10, fill = "dark green", outline = "linen", width = 10)
            canvas.create_line(mode.width/10, mode.height/2, mode.width*9/10,
                               mode.height/2, fill = "linen", width = 10)
            canvas.create_line(mode.width/2, mode.height/10, mode.width/2,
                               mode.height*9/10, fill = "linen", width = 10)
            canvas.create_text(mode.width/2-5, mode.height/11-5, text = "YOUR STATS", 
                               font = "Impact 100 bold", fill = "white")
            canvas.create_text(mode.width/2, mode.height/11, text = "YOUR STATS", 
                               font = "Impact 100 bold", fill = "dark red")
            mode.drawScoreStats(canvas)
            mode.drawFairwayStats(canvas)
            mode.drawStrokesGainedStats(canvas)
            mode.drawAveragePutts(canvas)

        canvas.create_rectangle(0, 0, mode.width, mode.height, 
								fill = "", width = 50, outline = "linen")
              

class Course(Mode):
    def appStarted(mode):
        homescreen = mode.loadImage("course.png")
        mode.homescreen = homescreen.transpose(Image.FLIP_LEFT_RIGHT)

        mode.helpx0 = (mode.width/30)*28
        mode.helpx1 = (mode.width/30)*29
        mode.helpy0 = mode.height/3
        mode.helpy1 = mode.height/2
        mode.helpMode = False

        mode.rows = None
        mode.cols = None
        mode.heightMargins = None
        mode.widthMargins = None

        mode.golfCourseName = None
        mode.golfCourseImage = None

        mode.foundCourse = False
        mode.currentHoleCoordinates = []
        mode.croppedImageCoordinates = {}

        mode.currentArea = None
        mode.hole = 0
        mode.holeCoordinates = {}

    
    def keyPressed(mode, event):
        if event.key == 'f':
            golfCourseName = mode.getUserInput("Enter Your Golf Course Name")
            if golfCourseName == None:
                mode.golfCourseName = golfCourseName
            else:
                mode.golfCourseName = golfCourseName
                mode.foundCourse = True
                mode.addCourse(mode.golfCourseName)
                mode.getGolfCourseImage()
                mode.getDimensions()
        if event.key == "b":
            mode.appStarted
        if event.key == 'n':
            if mode.hole != 0:
                mode.getImageCoordinates()
                mode.getCroppedHoleImage()
                mode.holeCoordinates[mode.hole] = mode.currentHoleCoordinates
            hole = mode.getUserInput("Enter Hole Number")
            if hole == None:
                mode.hole = mode.hole
            if hole.isdigit() == False:
                hole = mode.getUserInput("Please enter a number")
            if int(hole) > 18:
                hole = mode.getUserInput("Please enter a hole number between 1-18")
            else:
                mode.hole = int(hole)
                mode.currentHoleCoordinates = []
        if event.key == "h":
            mode.app.setActiveMode(mode.app.hole)

    def mousePressed(mode, event):
        if ((event.x >= mode.helpx0 and event.x <= mode.helpx1) and
			 (event.y >= mode.helpy0 and event.y <= mode.helpy1)) and mode.foundCourse:
             mode.app.setActiveMode(mode.app.courseModeHelp)
        if mode.hole != 0:
            mode.currentHoleCoordinates.append((event.x, event.y))
    
    def mouseDragged(mode, event):
        if mode.hole != 0:
            mode.currentHoleCoordinates.append((event.x, event.y))

    def mouseReleased(mode, event):
        if mode.hole != 0:
            mode.currentHoleCoordinates.append((event.x, event.y))

    def getPolygon(mode):
        mode.currentArea = Polygon(mode.currentHoleCoordinates)
    
    def getGolfCourseImage(mode):
        key = "Ai7Zvm84Npk6LkFoEUdLYHMR3VqxSSdSg-DXueNR9dQ9pdxE1DqI1ezLuCJvhlEt"
        url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/"
        size = "1100,1100"
        zoomLevel = "16"
        query = mode.golfCourseName.replace(" ", "%20")
        fullURL = url + query + "?mapSize=" + size + "&zoomLevel=" + zoomLevel + "&key=" + key
        #code from: https://kite.com/python/answers/how-to-download-an-image-using-requests-in-python
        r = requests.get(fullURL)
        file = open(f'{mode.golfCourseName}.png', "wb")
        file.write(r.content)
        file.close()

        #to save image with new and smaller dimensions to fit app dimensions
        #code from: https://auth0.com/blog/image-processing-in-python-with-pillow/
        image = Image.open(f'{mode.golfCourseName}.png')
        imageScaled = image.resize((750,750))
        imageScaled.save(f'{mode.golfCourseName}.png')

        #to load image into app attributes
        image1 = mode.loadImage(f'{mode.golfCourseName}.png')
        mode.golfCourseImage = image1
    
    def getDimensions(mode):
        image = mode.golfCourseImage
        w, h = image.size
        mode.rows = h 
        mode.cols = w
        mode.getMargins()

    def getMargins(mode):
        mode.heightMargins = (mode.height-mode.rows)/2
        mode.widthMargins = (mode.width - mode.cols)/2
    
    def getImageCoordinates(mode):
        imageCoordinates = []
        for x,y in mode.currentHoleCoordinates:
            newX, newY = y - mode.heightMargins,x - mode.widthMargins
            imageCoordinates.append((newX, newY))
        mode.croppedImageCoordinates[mode.hole] = imageCoordinates
    
    #code to crop Polygon from: https://gist.github.com/yosemitebandit/03bb3ae302582d9dc6be
    def getCroppedHoleImage(mode):
        im = Image.open(f'{mode.golfCourseName}.png').convert('RGBA')
        pixels = np.array(im)
        im_copy = np.array(im)

        region = Polygon(mode.croppedImageCoordinates[mode.hole])
        for index, pixel in np.ndenumerate(pixels):
            # Unpack the index.
            row, col, channel = index
            # We only need to look at spatial pixel data for one of the four channels.
            if channel != 0:
                continue
            point = Point(row, col)
            if not region.contains(point):
                im_copy[(row, col, 0)] = 255
                im_copy[(row, col, 1)] = 255
                im_copy[(row, col, 2)] = 255
                im_copy[(row, col, 3)] = 0

        cut_image = Image.fromarray(im_copy)
        cut_image.save(f'{mode.golfCourseName}Hole{mode.hole}.png')

    def addCourse(mode, course):
        courses = "courses.txt"

        with open(courses, "a") as text_file:
            text_file.write(mode.golfCourseName + ",")

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.homescreen))

        if mode.foundCourse == False:
            canvas.create_rectangle(mode.width/10, mode.height/10, mode.width*9/10, mode.height*9/10, 
								fill = "dark green", width = 20, outline = "linen")
            canvas.create_text(mode.width/2-5, mode.height/5-5, text = "ADD COURSES", 
                               font = "Impact 100 bold", fill = "white")
            canvas.create_text(mode.width/2, mode.height/5, text = "ADD COURSES", 
                               font = "Impact 100 bold")
            canvas.create_text(mode.width/2, mode.height/2, text = "Press 'f' to find course", 
                               font = "Impact 40 bold")
            canvas.create_rectangle(0, 0, mode.width, mode.height, 
								fill = "", width = 50, outline = "linen")
        else:
            canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.golfCourseImage))
            x0 = mode.helpx0
            y0 = mode.helpy0
            x1 = mode.helpx1
            y1 = mode.helpy1
            canvas.create_rectangle(x0, y0, x1, y1, fill = "linen", width = 3)
            canvas.create_text((x0 + x1)/2, (y0 + y1)/2, text = "H\nE\nL\nP", font = "Impact 20 bold")

        if mode.currentHoleCoordinates != []:
            canvas.create_polygon(mode.currentHoleCoordinates, fill = '', outline = "black", width=2)
        if mode.holeCoordinates != {}:
            for hole in mode.holeCoordinates:
                canvas.create_polygon(mode.holeCoordinates[hole], fill = '', outline = "black", width=2)

class CourseModeHelp(Mode):
    def appStarted(mode):
        homescreen = mode.loadImage("course.png")
        mode.homescreen = homescreen.transpose(Image.FLIP_LEFT_RIGHT)
        mode.backx0 = mode.width/10
        mode.backy0 = mode.height/10
        mode.backx1 = (mode.width/10) * 2
        mode.backy1 = mode.height/7

    def mousePressed(mode, event):
        if ((event.x >= mode.backx0 and event.x <= mode.backx1) and
			(event.y >= mode.backy0 and event.y <= mode.backy1)):
            mode.app.setActiveMode(mode.app.course)
            
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.homescreen))
        canvas.create_rectangle(mode.width/6, mode.height/6, mode.width*5/6, mode.height*5/6, 
								fill = "dark green", width = 20, outline = "linen")
    
        x0 = mode.backx0
        y0 = mode.backy0
        x1 = mode.backx1
        y1 = mode.backy1
        canvas.create_rectangle(x0, y0, x1, y1, fill = "linen", width = 3)
        canvas.create_text((x0 + x1)/2, (y0 + y1)/2, text = "BACK", font = "Impact 20 bold")
        canvas.create_text((mode.width)/2, mode.height/3, text = "Press 'n' to choose new hole to crop or recrop a hole",
                            font = "Impact 25")
        canvas.create_text((mode.width)/2, (mode.height*2)/3, text = "Press 'h' to edit marked holes",
                            font = "Impact 25")
        canvas.create_text((mode.width)/2, mode.height/2, text = "Holes that have already been cropped will be marked",
                            font = "Impact 25")
        canvas.create_rectangle(0, 0, mode.width, mode.height, 
								fill = "", width = 50, outline = "linen")
        
class Hole(Mode):
    def appStarted(mode):
        homescreen = mode.loadImage("course.png")
        mode.homescreen = homescreen.transpose(Image.FLIP_LEFT_RIGHT)

        mode.hole = 0
        mode.course = ""
        mode.image = None

        mode.rows = None
        mode.cols = None
        mode.heightMargins = None
        mode.widthMargins = None

        mode.top = False
        mode.leftTop = None
        mode.bottom = False
        mode.rightBottom = None

        mode.scale = 1.7

        mode.fairway = False
        mode.green = False

        mode.currGreenCoordinates = []
        mode.greenCoordinates = {}

        mode.currFairwaycoordinates = []
        mode.fairwayCoordinates = {}

        mode.par = {}

        mode.holeInformation = []

        mode.counter = 0

    def keyPressed(mode, event):
        if event.key == "F" and mode.course == "":
            course = mode.getUserInput("Enter Golf Course Name")
            if course == None:
                mode.course = mode.course
            else:
                mode.course = course

        if event.key == "B":
            mode.getHoleInformation()
            mode.makeDictionaryToCsv()   
            mode.app.setActiveMode(mode.app.playMode)

        if mode.course != "" and mode.hole <= 18:     
            if event.key == "n" and mode.hole < 18:
                if mode.hole > 0:
                    mode.getHoleInformation()
                    mode.greenCoordinates = {}
                    mode.fairwayCoordinates = {}
                    mode.leftTop = None
                    mode.rightBottom = None
                mode.hole += 1
                mode.getImage()
                mode.getHoleDimensions()
                mode.getMargins()
                par = mode.getUserInput("Enter Par")
                while par == None:
                    par = mode.getUserInput("Enter Par")
                mode.par[mode.hole] = par
            if event.key == "t":
                mode.top = True
            if event.key == "b":
                mode.bottom = True
            if event.key == "c":
                mode.getCroppedImage()
                mode.getHoleDimensions()
                mode.getScaledImage()
            if event.key == "r":
                mode.getRotatedImage()
            if event.key == "f":
                mode.fairway = True
            if event.key == "g":
                mode.green = True
        
    def mousePressed(mode, event):
        if mode.top == True:
            mode.leftTop = (event.x, event.y)
            mode.top = False
        if mode.bottom == True:
            mode.rightBottom = (event.x, event.y)
            mode.bottom = False
        if mode.green == True:
            mode.currGreenCoordinates.append((event.x, event.y))
            mode.counter += 1
        if mode.fairway == True:
            mode.currFairwaycoordinates.append((event.x, event.y))

    def mouseDragged(mode, event):
        mode.counter += 1
        if mode.green == True and mode.counter % 4 == 0:
            mode.currGreenCoordinates.append((event.x, event.y))
        if mode.fairway == True and mode.counter % 4 == 0:
            mode.currFairwaycoordinates.append((event.x, event.y))

    def mouseReleased(mode, event):
        if mode.green == True:
            mode.currGreenCoordinates.append((event.x, event.y))
            mode.getGreenCoordinates()
            mode.currGreenCoordinates = []
            mode.green = False
        if mode.fairway == True:
            mode.currFairwaycoordinates.append((event.x, event.y))
            mode.getFairwayCoordinates()
            mode.currFairwaycoordinates = []
            mode.fairway = False
        mode.counter = 0
    
    def getFairwayCoordinates(mode):
        coordinates = []
        for coordinate in mode.currFairwaycoordinates:
            x, y = mode.getImageCoordinates(coordinate)
            coordinates.append((x,y))
        if mode.hole in mode.fairwayCoordinates:
            mode.fairwayCoordinates[mode.hole].append(coordinates)
        else:
            mode.fairwayCoordinates[mode.hole] = [coordinates]

    def getGreenCoordinates(mode):
        coordinates = []
        for coordinate in mode.currGreenCoordinates:
            x, y = mode.getImageCoordinates(coordinate)
            coordinates.append((x, y))
        mode.greenCoordinates[mode.hole] = coordinates

    def getHoleInformation(mode):
        information = {}
        information["hole"] = mode.hole
        information["par"] = mode.par[mode.hole]
        information["green coordinates"] = mode.greenCoordinates[mode.hole]
        if mode.hole not in mode.fairwayCoordinates:
            information["fairway coordinates"] = []
        else:
            information["fairway coordinates"] = mode.fairwayCoordinates[mode.hole]
        mode.holeInformation.append(information)
    
    def getImage(mode):
        mode.image = mode.loadImage(f'{mode.course}Hole{mode.hole}.png')

    def getCroppedImage(mode):
        left, top = mode.getImageCoordinates(mode.leftTop)
        right, bottom = mode.getImageCoordinates(mode.rightBottom)
        imgCropped = mode.image.crop((left, top, right, bottom))
        imgCropped.save(f'{mode.course}Hole{mode.hole}.png')
        mode.getImage()
    
    def getScaledImage(mode):
        imgScaled = mode.scaleImage(mode.image, mode.scale)
        imgScaled.save(f'{mode.course}Hole{mode.hole}.png')
        mode.getImage()
        
    #rotate method from: https://note.nkmk.me/en/python-pillow-rotate/
    def getRotatedImage(mode):
        imgRotated = mode.image.rotate(90, resample=Image.BICUBIC, expand = True)
        imgRotated.save(f'{mode.course}Hole{mode.hole}.png')
        mode.getImage()
    
    def getImageCoordinates(mode, coordinates):
        x, y = coordinates
        newX, newY = x - mode.widthMargins,  y - mode.heightMargins
        return newX, newY

    def getHoleDimensions(mode):
        image = mode.image
        w, h = image.size
        mode.rows = h 
        mode.cols = w
        mode.getMargins()
    
    def getMargins(mode):
        mode.heightMargins = (mode.height - mode.rows)/2
        mode.widthMargins = (mode.width - mode.cols)/2
    
    #notes/code to create csv file from dictionary from: 
    # https://www.tutorialspoint.com/How-to-save-a-Python-Dictionary-to-CSV-file
    def makeDictionaryToCsv(mode):
        columnNames = ["hole", "par", "green coordinates", "fairway coordinates"]
        csvFile = f'{mode.course}Information.csv'
        try:
            with open(csvFile, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columnNames)
                writer.writeheader()
                for data in mode.holeInformation:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
    
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.homescreen))
        
        if mode.course == "":
            canvas.create_rectangle(mode.width/14, mode.height/6, mode.width*13/14, mode.height*5/6, 
								fill = "dark green", width = 20, outline = "linen")
            canvas.create_text(mode.width/2-5, mode.height/3-5, text = "HOLE EDITOR MODE",
                           font = "Impact 100 bold", fill = "white")
            canvas.create_text(mode.width/2, mode.height/3, text = "HOLE EDITOR MODE",
                           font = "Impact 100 bold")
            canvas.create_text(mode.width/2, mode.height/2, text = "Press 'F' to find course", 
                               font = "Impact 40 bold")
            canvas.create_rectangle(0, 0, mode.width, mode.height, 
								fill = "", width = 50, outline = "linen")
        if mode.course != "" and mode.image == None:
            canvas.create_rectangle(mode.width/14, mode.height/6, mode.width*13/14, mode.height*5/6, 
								fill = "dark green", width = 20, outline = "linen")
            canvas.create_text(mode.width/2, mode.height/2, text = "Press 'n' to begin",
                               font = "Impact 50 bold")
            canvas.create_rectangle(0, 0, mode.width, mode.height, 
								fill = "", width = 50, outline = "linen")
        if mode.course != "" and mode.image != None:
            canvas.create_rectangle(mode.width/10, 0, mode.width*9/10, mode.height, 
								fill = "dark green", width = 20, outline = "linen")
            canvas.create_text(mode.width/2-5, mode.height/12-5, text = f'Hole {mode.hole}',
                               font = "Impact 40 bold", fill = "white")
            canvas.create_text(mode.width/2, mode.height/12, text = f'Hole {mode.hole}',
                               font = "Impact 40 bold")
            canvas.create_text(mode.width/2, mode.height*11/12, text = "Press 'n' for next hole",
                               font = "Impact 30 bold")
            canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.image))
            canvas.create_text(mode.width/3, mode.height/7, 
                               text = '''To crop: press 't' for top left\nand then 'b' for bottom right then 'c to crop.\nPress 'r' to rotate.\nPress 'g' and outline green.\nPress 'f' and outline fairway.''',
                               font = "Impact 15")
        if mode.currGreenCoordinates != [] and mode.green:
            canvas.create_polygon(mode.currGreenCoordinates, fill = '', outline = "red", width=2)
        elif mode.currFairwaycoordinates != [] and mode.fairway:
            canvas.create_polygon(mode.currFairwaycoordinates, fill = '', outline = "blue", width=2)
        if mode.hole == 18:
            canvas.create_rectangle(mode.width*5/6, mode.height*5/6, mode.width*11/12, mode.height*11/12, fill = "linen", width = 0)
            canvas.create_text(mode.width/2, mode.height*5/6, text = "Press 'B' to go back",
                               font = "Impact 30 bold")
        

class UserExperienceApp(ModalApp):
    def appStarted(app):
        app.homescreenMode = HomescreenMode()
        app.aboutMode = AboutMode()
        app.playMode = PlayMode()
        app.statsMode = StatsMode()
        app.course = Course()
        app.courseModeHelp = CourseModeHelp()
        app.hole = Hole()
        app.setActiveMode(app.homescreenMode)
        
app = UserExperienceApp(width=900, height=750)