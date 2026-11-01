"""Validate this repository's Community Apps metadata without network access."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RAW = 'https://raw.githubusercontent.com/jbat66/unraid-templates/main/'


def validate():
    profile = ET.parse(ROOT / 'ca_profile.xml').getroot()
    assert profile.tag == 'CommunityApplications', 'Invalid profile root'
    assert (profile.findtext('Profile') or '').strip(), 'Empty repository Profile'
    assert (ROOT / 'LICENSE').read_text().strip(), 'Missing repository license'
    templates = sorted((ROOT / 'templates').glob('*.xml'))
    assert templates, 'No templates found'
    names = set()
    for path in templates:
        root = ET.parse(path).getroot()
        assert root.tag == 'Container' and root.get('version') == '2', path
        for tag in ('Name', 'Repository', 'Overview', 'Project', 'Support', 'Icon', 'WebUI'):
            assert (root.findtext(tag) or '').strip(), f'{path.name}: missing {tag}'
        name = root.findtext('Name')
        assert name not in names, f'Duplicate app: {name}'
        names.add(name)
        expected = RAW + path.relative_to(ROOT).as_posix()
        assert root.findtext('TemplateURL') == expected, f'{path.name}: noncanonical TemplateURL'
        if path.name == 'prusa-print-monitor.xml':
            configs = root.findall('Config')
            variables = [c for c in configs if c.get('Type') == 'Variable']
            assert [c.get('Target') for c in variables[:7]] == [
                'PRINTER_URL', 'API_USER', 'API_KEY', 'REFRESH_SECONDS', 'ALERT', 'CAMERA', 'CAMERA_URL']
            assert all(c.get('Display') == 'always' for c in configs)
            by_target = {c.get('Target'): c for c in configs}
            assert 'ALERT_SOUND_FILE' not in by_target
            assert by_target['CAMERA_URL'].get('Mask') == 'false'
            assert by_target['ALERT_REPEAT_SECONDS'].text == '60'
            assert by_target['DEFAULT_LAYOUT'].text == 'desktop'
            assert by_target['8085'].get('Type') == 'Port'
            assert by_target['/sounds'].get('Name') == 'Sounds Folder'
            assert by_target['/sounds'].get('Mode') == 'rw'
            assert by_target['SOUND_FILE'].text == '/mnt/user/appdata/prusa-print-monitor/sounds/AlarmSoundEffect.mp3'
            assert root.findtext('Repository') == 'ghcr.io/jbat66/prusa-print-monitor:latest'
            assert root.findtext('Support') == 'https://github.com/jbat66/Prusa-Print-Monitor/discussions/1'
        print(f'Valid: {path.relative_to(ROOT)}')
    print('Repository profile and license are present; all templates are valid.')


if __name__ == '__main__':
    validate()
