import os
import subprocess as sp
import stat

import utility

class BatchTool(object):
  '''
  Load existing batch templates, adjust and saves them, send job
  ''' 
  def __init__(self, path_templates, templates, arguments, batch, queue=None):

    self.batch          = batch
    self.path_templates = path_templates
    self.templates      = templates
    self.arguments      = arguments
    self.queue          = queue

    # make batch directory
    utility.make_directory(self.arguments['<path_batch>'])

  def make_scripts(self):

    # Loop over all the templates
    for _t in self.templates:

      # Open template
      _template = os.path.join( self.path_templates, _t)
      with open( _template, 'r') as _f:
        _template = _f.read()

      # make loop through all arguments and replace them
      for _arg, value in self.arguments.iteritems():
        _template = _template.replace( str(_arg), str(value))

      # Save new script
      _script = self.arguments['<path_batch_file_wo_ext>'] + '.' + _t.split('.')[-1]

      with open( _script, 'w') as _f:
        _f.write( _template)

  def send_job(self):

    # Change permission so that it can be executed 
    _sh = self.arguments['<path_batch_file_wo_ext>'] + '.sh'
    os.chmod(_sh, os.stat(_sh).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    if self.batch == 'condor':
      _txt      = self.arguments['<path_batch_file_wo_ext>'] + '.txt'
      _command  = ['condor_submit', _txt]
      utility.Print('status','{0}'.format(' '.join(_command)))
      print sp.check_output(_command)
    
    elif self.batch == 'lxbatch':
      _command  = ['bsub', '-q', self.queue, '-J', self.arguments['<path_batch_file_wo_ext>'] + ' < ' + _sh]
      utility.Print('status','{0}'.format(' '.join(_command)))
      print sp.check_output(_command)
