# Resume Builder Module

## Purpose

`PythonResumeBuilder/` is a self-contained module that helps generate resume content using JSON profile data and HTML templates.

It is intended to automate resume preparation with different layouts.

## Important assets

Key files include:

- `generate_resume.py`
- `resume.json`
- `template.html`
- `twenty_second_profile.json`
- `twenty_second_template.html`

## Application integration

The main app exposes the builder through:

- `/render_resume_builder`

That route reads:

- `PythonResumeBuilder/resume.json`
- `PythonResumeBuilder/template.html`

and passes both to `templates/resume_builder.html`.

## Candidate data

Your instruction specifically called out `resume.json` as the candidate’s data source. That file is the main structured input for resume generation.

## Architectural role

The resume builder is adjacent to the main job-application workflow rather than fully embedded in it.

It provides:

- reusable candidate profile content
- alternate visual resume layouts
- a natural extension point for future resume customization or export flows
