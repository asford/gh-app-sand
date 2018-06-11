import {set_zen, get_zen, handler } from './zen'
import { expect } from 'chai'
import 'mocha'

describe('zen function', () => {

  it('should return most recent zen or an empty mind', () => {
    expect(get_zen()).to.equal('The mind is a blank canvas.')

    set_zen("There is no being without nothingness.")
    expect(get_zen()).to.equal('There is no being without nothingness.')
  });

});
