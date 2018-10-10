#!/usr/bin/env python3
import subprocess
import pipes
import os


RAM = 10000
CORES = 6
STYLE = 'my-outdoor.TYP'
LANGUAGE = 'de'
BASE_DIR = './fzk-mde-garmin/Freizeitkarte-Entwicklung'


class MapBuilder(object):
    def __init__(self, map_to_build, output_name, build_args=None, needed_region=None, download_osm=True):
        self.map_to_build = map_to_build
        self.output_name = output_name
        self.build_args = []
        if build_args:
            self.build_args = build_args
        self.needed_region = needed_region
        self.download_osm = download_osm
        self.start_work()

    def start_work(self):
        if self.needed_region:
            run_step('create', self.map_to_build)
            if self.download_osm:
                run_step('create', self.needed_region)
                run_step('fetch_osm', self.needed_region)
            run_step('extract_osm', self.map_to_build)
        else:
            if self.download_osm:
                run_step('create', self.map_to_build)
                run_step('fetch_osm', self.map_to_build)
        run_step('fetch_ele', self.map_to_build)
        run_step('join', self.map_to_build)
        run_step('split', self.map_to_build)
        run_step('build', self.map_to_build, self.build_args)
        run_step('gmapsupp', self.map_to_build)

        file_name = self.move_map()
        self.apply_style(file_name)

        self.build_args.append('DEXPLORE')
        run_step('build', self.map_to_build, *self.build_args)
        run_step('gmapsupp', self.map_to_build)
        file_name = self.move_map(True)
        self.apply_style(file_name)
        self.log_build()


    def move_map(self, is_explore_map=False):
        name = self.output_name
        if is_explore_map:
            name += '-explore'
        name += '.img'
        subprocess.call(['mv', f'{BASE_DIR}/install/{self.map_to_build}_{LANGUAGE}/gmapsupp.img', f'output/{name}'])
        return name

    def apply_style(self, file_name):
        os.chdir('ReplaceTyp')
        subprocess.call(['./ReplaceTyp.sh', f'../output/{file_name}', STYLE])
        os.chdir('..')

    def log_build(self):
        safe_name = pipes.quote(self.map_to_build)
        subprocess.call([f'echo -e "`date +%d.%m.%Y\ %H:%M`: build {safe_name}\n$(cat updates)" > updates'], shell=True)


def run_step(*args):
    args = list(filter(None, args))
    os.chdir(BASE_DIR)
    subprocess.call(["perl", f"mt.pl" , f"--language={LANGUAGE}", f"--cores={CORES}", f"--ram={RAM}", *args])
    os.chdir('../..')


def build_test_map():
    map_name = 'test-map'
    os.chdir(BASE_DIR + '/tools/mkgmap/')
    subprocess.call(['java', '-jar', 'mkgmap.jar', f'--mapname={map_name}', 'test-map:all-elements'])
    subprocess.call(['rm', 'osmmap.img'])
    subprocess.call(['rm', 'osmmap.tdb'])
    subprocess.call(['mv', f'{map_name}.img', '../../../../output/'])
    os.chdir('../../../..')

if __name__ == '__main__':
    ## Alps, DEU+, BW
    MapBuilder('Freizeitkarte_ALPS', 'alps', 'DEXTENDEDROUTING', 'Freizeitkarte_EUROPE')
    MapBuilder('Freizeitkarte_DEU+', 'deutschland', needed_region='Freizeitkarte_EUROPE', download_osm=False)
    MapBuilder('Freizeitkarte_BADEN-WUERTTEMBERG', 'bw', needed_region='Freizeitkarte_EUROPE', download_osm=False)

    ## DEU+ and BW
    # MapBuilder('Freizeitkarte_DEU+', 'deutschland', needed_region='Freizeitkarte_EUROPE')
    # MapBuilder('Freizeitkarte_BADEN-WUERTTEMBERG', 'bw', needed_region='Freizeitkarte_EUROPE', download_osm=False)

    ## DEU and BW
    # MapBuilder('Freizeitkarte_DEU', 'deutschland')
    # MapBuilder('Freizeitkarte_BADEN-WUERTTEMBERG', 'bw', needed_region='Freizeitkarte_DEU', download_osm=False)

    ## Alles unabhängig
    # MapBuilder('Freizeitkarte_ALPS', 'alps', 'DEXTENDEDROUTING', 'Freizeitkarte_EUROPE')
    # MapBuilder('Freizeitkarte_DEU+', 'deutschland', needed_region='Freizeitkarte_EUROPE')
    # MapBuilder('Freizeitkarte_DEU', 'deutschland')
    # MapBuilder('Freizeitkarte_BADEN-WUERTTEMBERG', 'bw')
    # MapBuilder('Freizeitkarte_IRL', 'irland')
    # MapBuilder('Freizeitkarte_SAARLAND', 'saarland')
    # MapBuilder('Freizeitkarte_CHE', 'ch')
    # MapBuilder('Freizeitkarte_AUT', 'at')

