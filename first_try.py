#!/usr/bin/python
#
#=BEGIN GPL
#
# Copyright(c) 2009 Adriano Petrich
# http://github.com/frac/github-contest/tree/master
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 3 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#=END GPL
#

import psyco
#psyco.log()
psyco.full()
#psyco.profile(0.05, memory=100)
#psyco.profile(0.2)


def get_tanimoto(list1, list2):
    total = set(list1 + list2)
    return 1.0 * (len(list1) + len(list2) - len(total))/ len(total)

def write_recs(user, rankings):
    print rankings
    ranks = [sugestion for conf,sugestion,users in rankings]
    fd = open("results.txt", "a")
    fd.write("%s:%s\n"% (user, ",".join(ranks)))
    fd.close()

def write_ranks(user, rankings):
    fd = open("ranks.txt", "a")
    fd.write("%s:%s\n"% (user, str(rankings)))
    fd.close()


def rank_users(prefs, test_users):
  for person in test_users:
      total_users = {} #not used yet. important to normalize
      total_sim = {}
      for other in prefs.keys():
        # skip if its me
        if other == person: continue

        sim = get_tanimoto(prefs[person],prefs[other])
        #print person, other, sim

        if sim<=0: continue

        for item in prefs[other]:

          # ignore repos that I already have
          if item not in prefs[person]:
            total_users.setdefault(item,0)
            total_users[item]+= 1
#            print item, totals[item]

            # totalize scores
            total_sim.setdefault(item,0)
            total_sim[item]+=sim

      #list is still not normalized
      rankings=[(total_sim[item]/users,item,users) for item,users in total_users.items()]

      # sort by highest rank
      rankings.sort()
      rankings.reverse()

      rankings_pop=[(total_sim[item],item,users) for item,users in total_users.items()]
      rankings_pop.sort()
      rankings_pop.reverse()

      if len(rankings) > 0:
          best_guess = []
          best_guess += rankings_pop[:5]
          print len(rankings)
          for rank in rankings:
            if len(best_guess) >= 10:
                break
            if not( rank in best_guess ):
                best_guess.append(rank)



          print "saving user %s, %d"% (person, len(best_guess))
          #write_ranks(person, rankings)
          write_recs(person, best_guess)
      


if __name__ == '__main__':

    data_list = [line.strip().split(":") for line in file('base_data/data.txt')]
    #repos_list = [line.strip().split(":")[0] for line in file('base_data/repos.txt')]
    prefs = {}

    for pessoa, projeto in data_list:
        prefs.setdefault(pessoa,[])
        prefs[pessoa].append(projeto)

    test_users = [line.strip() for line in file('base_data/test.txt')]
    rank_users(prefs,test_users)


