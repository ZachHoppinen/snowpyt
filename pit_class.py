#!/usr/bin/python

'''
File defining a python class for snowpit data

November 2016, Simon Filhol
'''
from __future__ import division
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib._png import read_png


snowflake_dict = {'faceted':'snowflake/faceted.png',
                    'wind packed':'snowflake/wind_packed.png',
                    'horizontal ice layer':'snowflake/ice.png',
                    'clustered rounded':'snowflake/cluster_rounded.png',
                    'wind broken':'snowflake/wind_broken_precip.png',
                    'rounded':'snowflake/large_rounded.png',
                    'faceted and rounded':'snowflake/faceted_rounded.png',
                    'faceted rounded':'snowflake/faceted_rounded.png',
                    'rounded and faceted':'snowflake/rounding_faceted.png',
                    'rounded faceted':'snowflake/rounding_faceted.png',
                    'depth hoar':'snowflake/hollow_cups.png',
                    'melt refreeze':'snowflake/melt_freeze_crust.png',
                    'melt refreeze crust':'snowflake/melt_freeze_crust.png',
                    'partly decomposed': 'snowflake/partly_decomposed.png',
                    'dendrites':'snowflake/'}

class Snowpit(object):

    def __init__(self):
        self.date = '2001/08/10'
        self.East = 0
        self.North = 0
        self.Elevation = 0
        self.Observer = 'Bob'
        self.AirTemp = np.nan
        self.filename = 'example.txt'


class Snowpit_standard(Snowpit):
    '''
    Class for snowpit data as sorted by JC about Snow Svalbard Research
    '''

    def __init__(self, filename):
        super(Snowpit, self).__init__()
        self.filename = 'example.txt'

    def summary_plot(self, save=False):
        '''
        plot general snowpit plot
        :return:
        '''

        fig = plt.figure(figsize=(10, 10), dpi=150)
        # fig = plt.figure()
        ax1 = plt.subplot2grid((4,4),(0,0),rowspan = 3)
        ax2 = plt.subplot2grid((4,4),(0,1),rowspan = 3, sharey=ax1)  # Share y-axes with subplot 1
        ax3 = plt.subplot2grid((4,4),(0,2),rowspan = 3, sharey=ax2)
        ax4 = plt.subplot2grid((4,4),(0,3),rowspan = 3, sharey=ax3)

        # Set y-ticks of subplot 2 invisible
        plt.setp(ax2.get_yticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.setp(ax3.get_yticklabels(), visible=False)
        plt.setp(ax4.get_yticklabels(), visible=False)

        # Plot data
        fig.gca().invert_yaxis()
        im1 = ax1.plot(-self.snow_temperature, self.depth_temperature)

        im2 = ax2.barh(self.layer_top, np.repeat(1, self.layer_top.__len__()), self.layer_bot - self.layer_top,
                       color=cm.Blues(self.hardness_code / 6))
        ax2.set_xlim(0, 1)

        # include symbols

        for i, flake in enumerate(self.grain_type1.astype(str)):
            if flake != 'nan':
                im = plt.imread(snowflake_dict.get(flake))
                im[im == 0] = np.nan
                imagebox = OffsetImage(im, zoom=.02)
                if self.grain_type2.astype(str)[i] == 'nan':
                    hloc = 0.5
                else:
                    hloc = 0.33
                xy = [hloc,
                      ((self.layer_top[i] - self.layer_bot[i]) / 2 + self.layer_bot[i])]  # coordinates to position this image
                ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                ax2.add_artist(ab)

        for i, flake in enumerate(self.grain_type2.astype(str)):
            if flake != 'nan':
                im = plt.imread(snowflake_dict.get(flake))
                im[im == 0] = np.nan
                imagebox = OffsetImage(im, zoom=.02)
                xy = [0.66,
                      ((self.layer_top[i] - self.layer_bot[i]) / 2 + self.layer_bot[i])]  # coordinates to position this image
                ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                ax2.add_artist(ab)

        im3 = ax3.barh(self.layer_top, self.hardness_code, self.layer_bot - self.layer_top, color=cm.Blues(self.hardness_code / 6))
        ax3.set_xlim(0, 7)

        im4 = ax4.plot(self.density, self.depth_density)
        ax4.yaxis.tick_right()

        # add
        ax1.set_title("Temperature ($^\circ$C)")
        ax2.set_title("Stratigraphy")
        ax3.set_title("Hardness")
        ax4.set_title("Density")
        ax1.set_ylabel("Depth (cm)")

        ax1.grid()
        ax4.grid()

        metadata = "Date: " + self.date + '; Time [24hr]: ' + self.Time + '\n' + \
                   "Observer: " + self.Observer + '\n' + \
                   "Location description: " + self.General_loc + '\n' + \
                   "East : " + self.East + ' ' + self.East_unit + '\n' + \
                   "North: " + self.North + ' ' + self.North_unit + '\n' + \
                   "Elevation: " + self.Elevation + ' ' + self.Elevation_unit + '\n' + \
                   "Weather Conditions: " + self.weather_conditions + '\n' + \
                   "Air temperature: " + self.AirTemp + '$^{\circ}C$' '\n' + \
                   "Comments: " + self.comments + '\n'
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height

        plt.figtext(0.08, 0.15 , metadata,
                horizontalalignment='left',
                verticalalignment='center',wrap=True, fontsize=8)
        fig.autofmt_xdate()

        plt.tight_layout()
        plt.subplots_adjust(wspace=0)
        if save==True:
            fig.savefig(self.filename.split('/')[-1][0:-4])


    def plot_temperature(self):
        '''
        Plot temperature profile

        TODO:
            - reverse depth axis
        '''
        plt.figure()
        plt.plot(self.snow_temperature, self.depth_temperature)
        plt.gca().invert_yaxis()
        plt.xlabel('Temperature (C)')
        plt.ylabel('Depth (cm)')
        plt.title('Temperature profile')
        plt.grid()

    def plot_density(self):
        '''
        Plot density profile

        TODO:
            - reverse depth axis
        '''
        plt.figure()
        plt.plot(self.density, self.depth_density)
        plt.xlabel('Density (kg/m3)')
        plt.ylabel('Depth (cm)')
        plt.title('Density profile')
        plt.grid()

    def load_csv(self):
        self.load_metadata()
        self.load_profile()

    def load_profile(self):
        f = open(self.filename)
        for k,line in enumerate(f):
            if line[0:12] == 'Stratigraphy':
                break
        f.close()

        self.profile_raw_table = pd.read_csv(self.filename, sep='\t', skiprows=k+1)
        self.layerID = self.profile_raw_table.ix[:,0]
        self.layer_top = self.profile_raw_table.ix[:,1].astype(float)
        self.layer_bot = self.profile_raw_table.ix[:, 2].astype(float)

        self.grain_type1 = self.profile_raw_table.ix[:,3]
        self.grain_type2 = self.profile_raw_table.ix[:, 4]
        self.grain_size_min = self.profile_raw_table.ix[:, 5].astype(float)
        self.grain_size_max = self.profile_raw_table.ix[:, 6].astype(float)

        self.hardness = self.profile_raw_table.ix[:, 7]
        self.hardness_code = self.profile_raw_table.ix[:, 8].astype(float)

        self.depth_density = self.profile_raw_table.ix[:, 10].astype(float)
        self.density = self.profile_raw_table.ix[:, 11].astype(float)

        self.depth_temperature = self.profile_raw_table.ix[:,13].astype(float)
        self.snow_temperature = self.profile_raw_table.ix[:, 14].astype(float)

    def load_metadata(self):
        f = open(self.filename)
        try:
            for i, line in enumerate(f):
                if line[0:4] == 'Date':
                    self.date = line.split("\t")[1]
                if line[0:4] == 'Time':
                    self.Time = line.split("\t")[1]
                if line[0:4] == 'Gene':
                    self.General_loc = line.split("\t")[1]
                if line[0:4] == 'East':
                    self.East = line.split("\t")[1]
                    self.East_unit = line.split("\t")[2]
                if line[0:4] == 'Nort':
                    self.North = line.split("\t")[1]
                    self.North_unit = line.split("\t")[2]
                if line[0:4] == 'Elev':
                    self.Elevation = line.split("\t")[1]
                    self.Elevation_unit = line.split("\t")[2]
                if line[0:4] == 'Obse':
                    self.Observer = line.split("\t")[1]
                if line[0:4] == 'Air ':
                    self.AirTemp = line.split("\t")[1]
                if line[0:4] == 'Weat':
                    self.weather_conditions = line.split("\t")[1]
                if line[0:4] == 'Comm':
                    self.comments = line.split("\t")[1]
        except ValueError:
            print "Could not load metadata. Check file formating"
        f.close()

    def print_metadata(self):
        print "Date: " + self.date
        print "East [deg]: " + self.East
        print "North [deg]: " + self.North
        print "Elevation [m]: " + self.Elevation
        print "Observer: " + self.Observer
        print "Air temperature [C]: " + self.AirTemp
        print "Glacier: " + self.glacier
        print "Weather conditions: " + self.weather_conditions
        print "Comments: " + self.comments
class Snowpit_svalbard_JC(Snowpit):
    '''
    Class for snowpit data as sorted by JC about Snow Svalbard Research
    '''

    def __init__(self, filename):
        super(Snowpit, self).__init__()
        self.filename = 'example.txt'

    def summary_plot(self, save=False):
        '''
        plot general snowpit plot
        :return:
        '''

        fig = plt.figure(figsize=(10, 10), dpi=150)
        # fig = plt.figure()
        ax1 = plt.subplot2grid((4,4),(0,0),rowspan = 3)
        ax2 = plt.subplot2grid((4,4),(0,1),rowspan = 3, sharey=ax1)  # Share y-axes with subplot 1
        ax3 = plt.subplot2grid((4,4),(0,2),rowspan = 3, sharey=ax2)
        ax4 = plt.subplot2grid((4,4),(0,3),rowspan = 3, sharey=ax3)

        # Set y-ticks of subplot 2 invisible
        plt.setp(ax2.get_yticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.setp(ax3.get_yticklabels(), visible=False)
        plt.setp(ax4.get_yticklabels(), visible=False)

        # Plot data
        fig.gca().invert_yaxis()
        im1 = ax1.plot(-self.snow_temperature, self.depth_temperature)

        im2 = ax2.barh(self.layer_top, np.repeat(1, self.layer_top.__len__()), self.layer_bot - self.layer_top,
                       color=cm.Blues(self.hardness_code / 6))
        ax2.set_xlim(0, 1)

        # include symbols

        for i, flake in enumerate(self.grain_type1.astype(str)):
            if flake != 'nan':
                im = plt.imread(snowflake_dict.get(flake))
                im[im == 0] = np.nan
                imagebox = OffsetImage(im, zoom=.02)
                if self.grain_type2.astype(str)[i] == 'nan':
                    hloc = 0.5
                else:
                    hloc = 0.33
                xy = [hloc,
                      ((self.layer_top[i] - self.layer_bot[i]) / 2 + self.layer_bot[i])]  # coordinates to position this image
                ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                ax2.add_artist(ab)

        for i, flake in enumerate(self.grain_type2.astype(str)):
            if flake != 'nan':
                im = plt.imread(snowflake_dict.get(flake))
                im[im == 0] = np.nan
                imagebox = OffsetImage(im, zoom=.02)
                xy = [0.66,
                      ((self.layer_top[i] - self.layer_bot[i]) / 2 + self.layer_bot[i])]  # coordinates to position this image
                ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                ax2.add_artist(ab)

        im3 = ax3.barh(self.layer_top, self.hardness_code, self.layer_bot - self.layer_top, color=cm.Blues(self.hardness_code / 6))
        ax3.set_xlim(0, 7)

        im4 = ax4.plot(self.density, self.depth_density)
        ax4.yaxis.tick_right()

        # add
        ax1.set_title("Temperature ($^\circ$C)")
        ax2.set_title("Stratigraphy")
        ax3.set_title("Hardness")
        ax4.set_title("Density")
        ax1.set_ylabel("Depth (cm)")

        ax1.grid()
        ax4.grid()

        metadata = "Date: " + self.date + '\n' + \
                   "Observer: " + self.Observer + '\n' + \
                   "Glacier: " + self.glacier + '\n' + \
                   "East : " + self.East + '\n' + \
                   "North: " + self.North + '\n' + \
                   "Elevation: " + self.Elevation + '\n' + \
                   "Weather Conditions: " + self.weather_conditions + '\n' + \
                   "Air temperature: " + self.AirTemp + '\n' + \
                   "Comments: " + self.comments + '\n'
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height

        plt.figtext(0.08, 0.15 , metadata,
                horizontalalignment='left',
                verticalalignment='center',wrap=True, fontsize=8)
        fig.autofmt_xdate()

        plt.tight_layout()
        plt.subplots_adjust(wspace=0)
        if save==True:
            fig.savefig(self.filename.split('/')[-1][0:-4])


    def plot_temperature(self):
        '''
        Plot temperature profile

        TODO:
            - reverse depth axis
        '''
        plt.figure()
        plt.plot(self.snow_temperature, self.depth_temperature)
        plt.gca().invert_yaxis()
        plt.xlabel('Temperature (C)')
        plt.ylabel('Depth (cm)')
        plt.title('Temperature profile')
        plt.grid()

    def plot_density(self):
        '''
        Plot density profile

        TODO:
            - reverse depth axis
        '''
        plt.figure()
        plt.plot(self.density, self.depth_density)
        plt.xlabel('Density (kg/m3)')
        plt.ylabel('Depth (cm)')
        plt.title('Density profile')
        plt.grid()

    def load_csv(self):
        self.load_metadata()
        self.load_profile()

    def load_profile(self):
        self.profile_raw_table = pd.read_csv(self.filename, sep='\t', skiprows=14)
        self.layerID = self.profile_raw_table.ix[:,0]
        self.layer_top = self.profile_raw_table.ix[:,1]
        self.layer_bot = self.profile_raw_table.ix[:, 2]

        self.grain_type1 = self.profile_raw_table.ix[:,3]
        self.grain_type2 = self.profile_raw_table.ix[:, 4]
        self.grain_size_min = self.profile_raw_table.ix[:, 5]
        self.grain_size_max = self.profile_raw_table.ix[:, 6]

        self.hardness = self.profile_raw_table.ix[:, 7]
        self.hardness_code = self.profile_raw_table.ix[:, 8]

        self.depth_density = self.profile_raw_table.ix[:, 10]
        self.density = self.profile_raw_table.ix[:, 11]

        self.depth_temperature = self.profile_raw_table.ix[:,13]
        self.snow_temperature = self.profile_raw_table.ix[:, 14]



    def load_metadata(self):
        f = open(self.filename)
        try:
            for i, line in enumerate(f):
                if line[0:4] == 'Date':
                    self.date = line.split("\t")[1]
                    self.East = line.split("\t")[6]
                if line[0:4] == 'Time':
                    self.Elevation = line.split("\t")[5]
                if line[0:4] == 'Area':
                    self.North = line.split("\t")[7]
                if line[0:4] == 'Obse':
                    self.Observer = line.split("\t")[1]
                if line[0:4] == 'Air ':
                    self.AirTemp = line.split("\t")[2]
                if line[0:4] == 'Glac':
                    self.glacier = line.split("\t")[1]
                if line[0:4] == 'Glac':
                    self.weather_conditions = line.split("\t")[4]
                if line[0:4] == 'Gene':
                    self.comments = line.split("\t")[1]
        except ValueError:
            print "Could not load metadata. Check file formating"
        f.close()

    def print_metadata(self):
        print "Date: " + self.date
        print "East [deg]: " + self.East
        print "North [deg]: " + self.North
        print "Elevation [m]: " + self.Elevation
        print "Observer: " + self.Observer
        print "Air temperature [C]: " + self.AirTemp
        print "Glacier: " + self.glacier
        print "Weather conditions: " + self.weather_conditions
        print "Comments: " + self.comments

filename = '/home/arcticsnow/github/snowpyt/data_example/Standard_pit.csv'
a = Snowpit_standard(filename)
a.filename = filename
a.load_csv()
a.summary_plot(save=False)




