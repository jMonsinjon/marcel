#!/usr/bin/env python
# coding: utf-8

"""
Marcel is a french wrapper around the docker CLI, intended as a drop-in
replacement of docker, for the future french sovereign operating system.
"""

import subprocess
import sys
import re
import os
import six

from os.path import exists, join

__version__ = '0.1.0'

TRANSLATIONS = {
    # Commands
    u'chauffe': u'run',
    u'fais': u'exec',
    u'pousse': u'push',
    u'apporte': u'pull',
    u'bûches': u'logs',
    u'grève': u'suspend',
    u'matuer': u'kill',
    u'perquisitionne': u'inspect',
    u'construis': u'build',
    u'charge': u'load',
    u'plagie': u'copy',
    u'france24': u'info',
    u'insee': u'stats',
    u'rtt': u'pause',
    u'sur-ecoute': u'attach',
    u'cederoms': u'images',
    u'vos-papiers': u'login',
    u'déchéance': u'logout',
    u'sauvegarde': u'save',
    u'graffiti': u'tag',
    u'rsa': u'rmi',
    u'assigne-à-résidence': u'commit',
    u'roman-national': u'history',
    u'recycle': u'rm',
    u'cherche': u'search',
    u'réseau': u'network',
    u'marseille': u'port',
    u'renomme': u'rename',
    u'auboulot': u'unpause',
    u'barrage': u'wait',
    u'socialistes': u'ps',
    u'aide': u'help',
    u'monte-le-son': u'volume',
    u'récipient': u'container',
    # Options
    u'--aide': u'--help',
    u'--graffiti': u'--tag',
    u'--sortie': u'--output',
    u'--auteur': u'--author',
    u'--49-3': u'--force',
    u'--etat-d-urgence': u'--privileged',
    u'--disque-numerique-polyvalent': u'--dvd'
}

MARCELFILE_TRANSLATIONS = {
    u'DEPUIS': u'FROM',
    u'CRÉATEUR': u'MAINTAINER',
    u'LANCE': u'RUN',
    u'ORDRE': u'CMD',
    u'ÉTIQUETTE': u'LABEL',
    u'DÉSIGNER': u'EXPOSE',
    u'EELV': u'ENV',
    u'AJOUTER': u'ADD',
    u'COPIER': u'COPY',
    u'POINT D\'ENTRÉE': u'ENTRYPOINT',
    u'UTILISATEUR': u'USER',
    u'LIEU DE TRAVAIL': u'WORKDIR',
    u'BTP': u'ONBUILD',
    u'APÉRITIF': u'STOPSIGNAL',
}


def translate_marcelfile(marcelfile):
    """
    Converts a RecetteÀMarcel to a Dockerfile

    :param input_file: Input filename
    :param output_file: Output filename
    :return: The translated Dockerfile as a string
    """

    for key in MARCELFILE_TRANSLATIONS:
        expression = re.compile(r'(^|\n)%s' % key, re.UNICODE)
        marcelfile = expression.sub(r"\1%s" % MARCELFILE_TRANSLATIONS[key], marcelfile)
    return marcelfile


def use_marcelfile(command):
    """
    Detect if a RecettesÀMarcel file is present in the current directory.
    If so, inject a "-f ./RecettesÀMarcel" argument in the docker build command,
    if such an argument was not already passed.
    """
    curdir = os.getcwd()
    marcelfile_path = join(curdir, u'RecetteÀMarcel')
    dockerfile_path = join(curdir, u'.RecetteÀMarcel.Dockerfile')
    if not exists(marcelfile_path) or '-f' in command:
        return command

    # We want to generate a file with the proper Dockerfile format
    with open(marcelfile_path) as marcelfile,  open(dockerfile_path, 'w') as dockefile:
        marcelfile_content = marcelfile.read()
        if six.PY2:  # pragma: no cover
            marcelfile_content = marcelfile_content.decode('utf-8')
        translated_marcelfile = translate_marcelfile(marcelfile_content)
        if six.PY2:  # pragma: no cover
            translated_marcelfile = translated_marcelfile.encode('utf-8')
        dockefile.write(translated_marcelfile)
    command = command[:2] + ['-f', u'./.RecetteÀMarcel.Dockerfile'] + command[2:]
    return command


def print_marcelhelp():
    """Build the help message to print as an executable command."""
    command = ['echo']
    command = command + ['Utilisation:   marcel [OPTIONS] COMMAND ', '\n']
    command = command + ['\n']
    command = command + ['Le Docker à la française !', '\n']
    command = command + ['\n']
    command = command + ['Options :', '\n']
    command = command + ['      --aide                          ', 'Vient au secoursde l\'utilisateur', '\n']
    command = command + ['      --auteur                        ', 'Permet de préciser le nom du propriétaire intellectuel de l\'oeuvre', '\n']
    command = command + ['      --sortie                        ', '--output', '\n']
    command = command + ['      --49-3                          ', 'Décision unilatérale permettant d\'assurer l\'exécution de la procédure', '\n']
    command = command + ['      --etat-d-urgence                ', 'Desormais, je fais ce qu\'il me plait', '\n']
    command = command + ['      --disque-numerique-polyvalent   ', '--dvd', '\n']
    command = command + ['\n']

    command = command + ['Groupes de directives :', '\n']
    # command = command + ['  checkpoint            ', 'Gestion des  checkpoints', '\n']
    # command = command + ['  config                ', 'Gestion des  Docker configs', '\n']
    command = command + ['  récipient             ', 'Placard', '\n']
    command = command + ['  cédérom               ', 'Médiathèque', '\n']
    command = command + ['  réseau                ', 'Point de rassemblement', '\n']
    # command = command + ['  node                  ', 'Gestion des  Swarm nodes', '\n']
    # command = command + ['  plugin                ', 'Gestion des  plugins', '\n']
    # command = command + ['  secret                ', 'Gestion des  Docker secrets', '\n']
    # command = command + ['  service               ', 'Gestion des  services', '\n']
    # command = command + ['  stack                 ', 'Gestion des  Docker stacks', '\n']
    # command = command + ['  swarm                 ', 'Gestion des  Swarm', '\n']
    # command = command + ['  system                ', 'Gestion des  Docker', '\n']
    # command = command + ['  trust                 ', 'Gestion des  trust on Docker images', '\n']
    command = command + ['  monte-le-son          ', 'Table de mixage', '\n']
    command = command + ['\n']

    command = command + ['Directives :', '\n']
    command = command + ['  chauffe               ', 'Démarre un nouveau récipient', '\n']
    command = command + ['  fais                  ', 'Exécute une nouvelle directive dans un récipient existant', '\n']
    command = command + ['  pousse                ', 'Envoi un cédérom dans la médiathèque', '\n']
    command = command + ['  apporte               ', 'Récupère un cédérom de la médiathèque', '\n']
    command = command + ['  bûches                ', 'Invite les bûches d\'un récipient', '\n']
    command = command + ['  grève                 ', 'Arrêt du travail pour cause de revendications mutiples. Sortez les barbecues !', '\n']
    command = command + ['  matuer                ', 'Assassine sauvagement un récipient', '\n']
    command = command + ['  perquisitionne        ', 'Récupère les informations de chaque objet Marcel', '\n']
    command = command + ['  construis             ', 'Grave un nouveau cédérom', '\n']
    command = command + ['  charge                ', 'Copie un cédérom depuis un disque local', '\n']
    # command = command + ['  plagie                ', 'copy', '\n']
    command = command + ['  france24              ', 'Retransmet les informations essentielles à propos de Marcel', '\n']
    # command = command + ['  insee                 ', 'stats', '\n']
    command = command + ['  rtt                   ', 'Donne une pause bien méritée au récipient', '\n']
    # command = command + ['  sur-ecoute            ', 'attach', '\n']
    command = command + ['  cederoms              ', 'Affiche la liste des cédéroms de la médiathèque locale', '\n']
    command = command + ['  vos-papiers           ', 'Montre pâte blanche auprès de ces messieurs les gendarmes', '\n']
    # command = command + ['  déchéance             ', 'logout', '\n']
    command = command + ['  sauvegarde            ', 'Copie un cédérom sur un support amovible', '\n']
    command = command + ['  graffiti              ', 'Dessine un nom sur un cédérom', '\n']
    command = command + ['  rsa                   ', 'Supprime un cédérom de la médiathèque locale', '\n']
    command = command + ['  assigne-à-résidence   ', 'Grave un cédérom à partir d\'un récipient existant', '\n']
    command = command + ['  roman-national        ', 'Affiche toute l\'histoire d\'un cédérom', '\n']
    command = command + ['  recycle               ', 'Supprime un récipient', '\n']
    command = command + ['  cherche               ', 'Envoi Lycos pour trouver un cédérom à la médiathèque du coin de la rue', '\n']
    # command = command + ['  marseille             ', 'port', '\n']
    # command = command + ['  renomme               ', 'rename', '\n']
    command = command + ['  auboulot              ', 'Remet au boulot un récipient en grève', '\n']
    command = command + ['  barrage               ', 'Empêche un récipient d\'avancer jusqu\'à ce qu\'il capitule', '\n']
    command = command + ['  socialistes           ', 'Affiche la liste des récipients actifs', '\n']
    command = command + ['  aide                  ', 'Vient au secours de l\'utilisateur', '\n']
    return command
    

def replace_command(command):
    """Replace the executable itself for given values of the first command."""
    if len(command) > 1 and command[1] == 'et-son-orchestre':
        command.pop(0)
        command[0] = 'docker-compose'
    else:
        command[0] = 'docker'

    if len(command) == 1:
        command.append('help')
    return command


def translate_command(command):
    """Translate the french parts of the command to docker syntax."""
    command = replace_command(command)
    return [TRANSLATIONS.get(chunk, chunk) for chunk in command if chunk]


def build_command(command):
    """Translate the command from marcel syntax to docker."""
    command = translate_command(command)
    if len(command) > 1:
        subcommand = command[1]
        if subcommand == 'build':
            command = use_marcelfile(command)
        elif subcommand == 'help':
            command = print_marcelhelp()
    return command


def main():  # pragma: no cover
    """Run docker commands from marcel syntax."""
    subprocess.call(build_command(sys.argv))


if __name__ == '__main__':   # pragma: no cover
    main()
