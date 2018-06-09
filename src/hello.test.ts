import hello from './hello_world';
import { expect } from 'chai';
import 'mocha';

describe('Hello function', () => {

  it('should return hello cruel world', () => {
    const result = hello();
    expect(result).to.equal('Hello cruel world!');
  });

});
