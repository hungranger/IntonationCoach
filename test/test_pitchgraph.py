import json
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pitchgraph import get_praat_pitch, format_pitch_data, smooth_pitch_data


class PitchgraphTestCase(unittest.TestCase):
    """Tests for pitchgraph.py"""

    def setUp(self):
        self.audio_file = os.path.abspath('static/sounds/en-us-1.wav')

    def test_get_praat_pitch_format(self):
        """Does get_praat_pitch return a dict of the format expected by format_pitch_data?"""

        pitch_data = get_praat_pitch(self.audio_file)
        self.assertIsInstance(pitch_data, dict)

        akey = pitch_data.iterkeys().next()
        value_dict = pitch_data[akey]
        self.assertIsInstance(akey, float)
        self.assertIsInstance(value_dict, dict)
        self.assertIn("Pitch", value_dict)

    def test_format_pitch_data(self):
        """Does format_pitch_data return a list of dicts that contain "x" and "y" as keys?"""

        formatted_pitch_data = format_pitch_data(get_praat_pitch(self.audio_file))
        self.assertIsInstance(formatted_pitch_data, list)
        self.assertIsInstance(formatted_pitch_data[0], dict)
        self.assertIn("x", formatted_pitch_data[0])
        self.assertIn("y", formatted_pitch_data[0])

    def test_smooth_pitch_data(self):
        """Does smooth_pitch_data reduce the number of datapoints?"""

        unsmoothed = format_pitch_data(get_praat_pitch(self.audio_file))
        smoothed = json.loads(smooth_pitch_data(unsmoothed))
        self.assertLess(len(smoothed), len(unsmoothed))

    def test_empty_if_no_audio_captured(self):
        """Does smooth_pitch_data return an empty list (in a JSON string)
        if no audio was captured?"""

        smoothed = json.loads(smooth_pitch_data([]))
        self.assertEqual(smoothed, [])


if __name__ == "__main__":
    unittest.main()
